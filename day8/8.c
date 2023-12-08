#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <sys/stat.h>

#define LEFT 0
#define RIGHT 1
#define MAX_INSTRUCTIONS 300
#define MAPSIZE 26 * 26 * 26
#define HASH(kstr)                                                             \
  ((kstr[0] - 'A') * 26 * 26 + (kstr[1] - 'A') * 26 + (kstr[2] - 'A'))

typedef uint16_t key;
typedef key map[2][MAPSIZE];

void parse_input(char *input, uint16_t *instructions, size_t *num_instructions,
                 map node_map) {
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
  char *key_tok = strtok(NULL, " =(),\n");
  while (NULL != key_tok) {
    char *ltok = strtok(NULL, " =(),\n");
    char *rtok = strtok(NULL, " =(),\n");
    printf("keyset %s %s %s\n", key_tok, ltok, rtok);
    node_map[LEFT][HASH(key_tok)] = HASH(ltok);
    node_map[RIGHT][HASH(key_tok)] = HASH(rtok);
    key_tok = strtok(NULL, " =(),\n");
  }
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
  uint16_t instructions[MAX_INSTRUCTIONS];
  size_t num_instructions;
  parse_input(input_txt, instructions, &num_instructions, node_map);
  uint64_t instr_i = 0;
  uint64_t nsteps = 0;
  key start_key = HASH("AAA");
  while (start_key != HASH("ZZZ")) {
    uint16_t inst = instructions[instr_i % num_instructions];
    start_key = node_map[inst][start_key];
    nsteps++;
    instr_i++;
  }
  printf("nsteps: %llu \n", nsteps);

  return EXIT_SUCCESS;
}
