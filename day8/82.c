#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <sys/stat.h>
#include <time.h>

#define LEFT 0
#define RIGHT 1
#define MAX_INSTRUCTIONS 300
#define MAPSIZE 26 * 26 * 26
#define ZHASH 'Z' - 'A'
#define MAX_PATHKEYS_LEN                                                       \
  6 // not totallly generalizable but seems like true for all inputs
#define HASH(kstr)                                                             \
  ((kstr[0] - 'A') * 26 * 26 + (kstr[1] - 'A') * 26 + (kstr[2] - 'A'))

typedef uint16_t key;
typedef key map[2][MAPSIZE];

void parse_input(char *input, uint16_t *instructions, size_t *num_instructions,
                 key *path_keys, uint8_t *num_pks, map node_map) {
  char *inst_str = strtok(input, " =(),\n");
  int i = 0;
  uint16_t *iptr;
  char c;
  size_t inst_cntr = 0;
  while ((c = *inst_str++) && (iptr = instructions++)) {
    if (c == 'L') {
      *iptr = LEFT;
    } else {
      *iptr = RIGHT;
    }
    inst_cntr++;
    printf("%c %d, ", c, *iptr);
  }
  *num_instructions = inst_cntr;
  printf("\n");

  uint8_t npk = 0;
  char *key_tok = strtok(NULL, " =(),\n");
  while (NULL != key_tok) {
    char *ltok = strtok(NULL, " =(),\n");
    char *rtok = strtok(NULL, " =(),\n");
    printf("keyset %s %s %s\n", key_tok, ltok, rtok);
    node_map[LEFT][HASH(key_tok)] = HASH(ltok);
    node_map[RIGHT][HASH(key_tok)] = HASH(rtok);
    if (key_tok[2] == 'A') {
      path_keys[npk] = HASH(key_tok);
      npk++;
    }
    key_tok = strtok(NULL, " =(),\n");
  }
  *num_pks = npk;
}

void read_file(char *ret_txt, const char *fname, const size_t fsize,
               const size_t strsize) {
  FILE *inputf = fopen(fname, "rb");
  if (!inputf) {
    printf("Couldn't open file %s\n", fname);
    exit(EXIT_FAILURE);
  }

  int bytes_read = fread(ret_txt, 1, fsize, inputf);
  if (bytes_read == -1) {
    printf("error reading file %s", fname);
    perror("Error");
    fclose(inputf);
    exit(EXIT_FAILURE);
  }
  ret_txt[strsize - 1] = '\0';
  fclose(inputf);
}

int main(int argc, char *argv[]) {
  char *fname = "./sample3.txt";
  if (argc > 1) {
    fname = argv[1];
  }
  struct stat input_st;
  if (stat(fname, &input_st)) {
    printf("Couldn't stat %s\n", fname);
    exit(EXIT_FAILURE);
  }

  size_t txtsize = input_st.st_size + 1;

  char input_txt[txtsize];

  read_file(input_txt, fname, input_st.st_size, txtsize);

  map node_map;
  key path_keys[MAX_PATHKEYS_LEN];
  uint16_t instructions[MAX_INSTRUCTIONS];
  size_t num_instructions;
  uint8_t num_pks;
  parse_input(input_txt, instructions, &num_instructions, path_keys, &num_pks,
              node_map);
  printf("npks: %d\n", num_pks);
  uint64_t instr_i = 0;
  uint64_t nsteps = 0;
  time_t start_time_sec = time(NULL), end_time_sec;
  while (1) {
    if ((nsteps & (1024 * 1024 * 1024 - 1)) == 0) {
      end_time_sec = time(NULL);
      printf("~1billion steps taking: %f seconds\n",
             difftime(end_time_sec, start_time_sec));
      start_time_sec = end_time_sec;
      printf("At step: %llu\n", nsteps);
      printf("pathkeys checkpoint: ");
      for (int i=0; i < num_pks; i++){
        printf("%d ", path_keys[i]);
      }
      printf("\n");
    }
    uint16_t inst = instructions[instr_i % num_instructions];
    for (int i = 0; i < num_pks; i++) {
      path_keys[i] = node_map[inst][path_keys[i]];
    }
    nsteps++;
    uint8_t allz = 1;
    for (int i = 0; allz && i < num_pks; i++) {
      allz = (allz && (ZHASH == path_keys[i] % 26));
    }
    if (allz) {
      break;
    }
    instr_i++;
  }
  printf("Answer nsteps: %llu \n", nsteps);

  return EXIT_SUCCESS;
}
