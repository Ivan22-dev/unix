/***************************************************************************//**

  @file         main.c

  @author       Stephen Brennan

  @date         Thursday,  8 January 2015

  @brief        LSH (Libstephen SHell)

*******************************************************************************/

#include <sys/wait.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <dirent.h>
#include <fcntl.h>
void formatError();

/*
  Function Declarations for builtin shell commands:
 */

int lsh_cd(char **args);
int lsh_help(char **args);
int lsh_exit(char **args);
int lsh_ls(char **args);
int lsh_pwd(char **args);
int lsh_mv(char **args);
int lsh_mkdir(char **args);
int lsh_touch(char **args);

/*
  List of builtin commands, followed by their corresponding functions.
 */
char *builtin_str[] = {
  "cd",
  "help",
  "exit",
  "ls",
  "pwd",
  "mv",
  "mkdir",
  "touch"
};

int (*builtin_func[]) (char **) = {
  &lsh_cd,
  &lsh_help,
  &lsh_exit,
  &lsh_ls,
  &lsh_pwd,
  &lsh_mv,
  &lsh_mkdir,
  &lsh_touch
 
};

int lsh_num_builtins() {
  return sizeof(builtin_str) / sizeof(char *);
}

/*
  Builtin function implementations.
*/

/**
   @brief Bultin command: change directory.
   @param args List of args.  args[0] is "cd".  args[1] is the directory.
   @return Always returns 1, to continue executing.
 */




int lsh_cd(char **args)
{
  if (args[1] == NULL) {
    fprintf(stderr, "lsh: expected argument to \"cd\"\n");
  } else {
    if (chdir(args[1]) != 0) {
      perror("lsh");
    }
  }
  return 1;
}

/**
   @brief Builtin command: print help.
   @param args List of args.  Not examined.
   @return Always returns 1, to continue executing.
 */
int lsh_help(char **args)
{
  int i;
  printf("Stephen Brennan's LSH\n");
  printf("Type program names and arguments, and hit enter.\n");
  printf("The following are built in:\n");

  for (i = 0; i < lsh_num_builtins(); i++) {
    printf("  %s\n", builtin_str[i]);
  }

  printf("Use the man command for information on other programs.\n");
  return 1;
}

/**
   @brief Builtin command: exit.
   @param args List of args.  Not examined.
   @return Always returns 0, to terminate execution.
 */
int lsh_exit(char **args)
{
  return 0;
}

/*MY FUNCTION*/
int lsh_ls(char **args)
{
    DIR *mydir;
    struct dirent *myfile;
    struct stat mystat;

    char buf[512];
    if (args[1] == NULL){
	mydir = opendir(".");
	 while((myfile = readdir(mydir)) != NULL)
    {
        sprintf(buf, "%s/%s", args[1], myfile->d_name);
        stat(buf, &mystat);
        printf(" %s\n", myfile->d_name);
    }
	fprintf(stderr, "Expected arguments after command ls\n");
	return 1;
    }
    mydir = opendir(args[1]);
    if (mydir == NULL){
	printf("No file in directory\n");
	return 1;
	}
    while((myfile = readdir(mydir)) != NULL)
    {
	sprintf(buf, "%s/%s", args[1], myfile->d_name);
        stat(buf, &mystat);
        /*printf("%zu",mystat.st_size);*/
        printf(" %s\n", myfile->d_name);
    }
	closedir(mydir);
	return 1;
}


#ifdef __unix__
    #define IS_POSIX 1
    #include <unistd.h>
#else
    #define IS_POSIX 0
#endif


int lsh_pwd ( char **args)
{
    if (IS_POSIX == 1) {
        char cwd[1024];
        getcwd(cwd, sizeof(cwd));
        printf("%s\n", cwd);
    }
    return 1;
}

#define SBUF 256
#define DBUF 256

int lsh_mv(char **args)
    {
      DIR* dir_ptr;     // the directory
      struct dirent* direntp;


      if( args[2] == NULL )
      {
        printf("Usage:  %s MOVE\n", args[0] );
        return 1;
      }
	
      if(args[1] == NULL && args[2] == NULL)
      {
        printf("Error! few arguments provided\n " );
        return 1;
      }

        char src_folder[SBUF];
        char dest_folder[DBUF];
        strcpy(src_folder, args[1]);
        strcpy(dest_folder, args[2]);
	  dir_ptr = opendir("."); //open directory
        if ( dir_ptr == NULL )
        {
            perror( "." );
            return 1;
        }

        while( (direntp = readdir( dir_ptr )) != NULL ) 
        {
            if (  strcmp(direntp->d_name, dest_folder) !=0) //search file or directory
            {
			printf("found the file %s\n", dest_folder);

                break;
            }else
                printf("not found\n");
                break;
        }
        rename(src_folder, dest_folder);
        closedir( dir_ptr );

        return 1;
  }

int lsh_mkdir(char **args)
 
{
 
 
    if(mkdir(args[1],0777)==-1)//creating a directory

    {

        printf("Error\n");
        return 1;
    }
   else{
		printf("Directory created\n");
	}
}


int lsh_touch(char **args){
	int i=1;
	int f=open(args[1],O_WRONLY|O_APPEND|O_CREAT,0777);
	close(f);
	i++;
	return 1;

}


/**
  @brief Launch a program and wait for it to terminate.
  @param args Null terminated list of arguments (including program).
  @return Always returns 1, to continue execution.
 */
int lsh_launch(char **args)
{
  pid_t pid;
  int status;

  pid = fork();
  if (pid == 0) {
    // Child process
    if (execvp(args[0], args) == -1) {
      perror("lsh");
    }
    exit(EXIT_FAILURE);
  } else if (pid < 0) {
    // Error forking
    perror("lsh");
  } else {
    // Parent process
    do {
      waitpid(pid, &status, WUNTRACED);
    } while (!WIFEXITED(status) && !WIFSIGNALED(status));
  }

  return 1;
}

/**
   @brief Execute shell built-in or launch program.
   @param args Null terminated list of arguments.
   @return 1 if the shell should continue running, 0 if it should terminate
 */
int lsh_execute(char **args)
{
  int i;

  if (args[0] == NULL) {
    // An empty command was entered.
    return 1;
  }

  for (i = 0; i < lsh_num_builtins(); i++) {
    if (strcmp(args[0], builtin_str[i]) == 0) {
      return (*builtin_func[i])(args);
    }
  }

  return lsh_launch(args);
}

/**
   @brief Read a line of input from stdin.
   @return The line from stdin.
 */
char *lsh_read_line(void)
{
#ifdef LSH_USE_STD_GETLINE
  char *line = NULL;
  ssize_t bufsize = 0; // have getline allocate a buffer for us
  if (getline(&line, &bufsize, stdin) == -1) {
    if (feof(stdin)) {
      exit(EXIT_SUCCESS);  // We recieved an EOF
    } else  {
      perror("lsh: getline\n");
      exit(EXIT_FAILURE);
    }
  }
  return line;
#else
#define LSH_RL_BUFSIZE 1024
  int bufsize = LSH_RL_BUFSIZE;
  int position = 0;
  char *buffer = malloc(sizeof(char) * bufsize);
  int c;

  if (!buffer) {
    fprintf(stderr, "lsh: allocation error\n");
    exit(EXIT_FAILURE);
  }

  while (1) {
    // Read a character
    c = getchar();

    if (c == EOF) {
      exit(EXIT_SUCCESS);
    } else if (c == '\n') {
      buffer[position] = '\0';
      return buffer;
    } else {
      buffer[position] = c;
    }
    position++;

    // If we have exceeded the buffer, reallocate.
    if (position >= bufsize) {
      bufsize += LSH_RL_BUFSIZE;
      buffer = realloc(buffer, bufsize);
      if (!buffer) {
        fprintf(stderr, "lsh: allocation error\n");
        exit(EXIT_FAILURE);
      }
    }
  }
#endif
}

#define LSH_TOK_BUFSIZE 64
#define LSH_TOK_DELIM " \t\r\n\a"
/**
   @brief Split a line into tokens (very naively).
   @param line The line.
   @return Null-terminated array of tokens.
 */
char **lsh_split_line(char *line)
{
  int bufsize = LSH_TOK_BUFSIZE, position = 0;
  char **tokens = malloc(bufsize * sizeof(char*));
  char *token, **tokens_backup;

  if (!tokens) {
    fprintf(stderr, "lsh: allocation error\n");
    exit(EXIT_FAILURE);
  }

  token = strtok(line, LSH_TOK_DELIM);
  while (token != NULL) {
    tokens[position] = token;
    position++;

    if (position >= bufsize) {
      bufsize += LSH_TOK_BUFSIZE;
      tokens_backup = tokens;
      tokens = realloc(tokens, bufsize * sizeof(char*));
      if (!tokens) {
		free(tokens_backup);
        fprintf(stderr, "lsh: allocation error\n");
        exit(EXIT_FAILURE);
      }
    }

    token = strtok(NULL, LSH_TOK_DELIM);
  }
  tokens[position] = NULL;
  return tokens;
}

/**
   @brief Loop getting input and executing it.
 */
void lsh_loop(void)
{
  char *line;
  char **args;
  int status;

  do {
    printf(">> ");
    line = lsh_read_line();
    args = lsh_split_line(line);
    status = lsh_execute(args);

    free(line);
    free(args);
  } while (status);
}

/**
   @brief Main entry point.
   @param argc Argument count.
   @param argv Argument vector.
   @return status code
 */
int main(int argc, char **argv)
{
  // Load config files, if any.

  // Run command loop.
  lsh_loop();

  // Perform any shutdown/cleanup.

  return EXIT_SUCCESS;
}

