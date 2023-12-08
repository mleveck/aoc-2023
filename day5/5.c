#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <sys/stat.h>

#define TABLE_CAP 96
#define NTABLES 7
#define MAX_SEEDS_N 32

typedef struct row {
  int64_t dst;
  int64_t src;
  int64_t size;
} row;

typedef struct range {
  int64_t start;
  int64_t stop;
} range;

typedef struct table {
  int64_t len;
  row rows[TABLE_CAP];
} table;

typedef struct seeds {
  int64_t len;
  int64_t seed[MAX_SEEDS_N];
} seeds;

void print_row(const row* r) { printf("%lld, %lld, %lld\n", r->dst, r->src, r->size); }

void print_table(const table* t) {
  for (int i = 0; i < t->len; i++) {
    print_row(&t->rows[i]);
  }
}

void parse_seeds(char *s, seeds *seeds) {
  char *tok;
  int64_t *p = seeds->seed;
  tok = strtok(s, ":\n ");    // get rid of "seeds:"
  tok = strtok(NULL, " :\n"); // now starting on seed number
  int64_t len = 0;
  while ('a' >= *tok || 'z' <= *tok) {
    *p++ = strtoll(tok, NULL, 10);
    len++;
    tok = strtok(NULL, " :\n");
  }
  seeds->len = len;
  tok = strtok(NULL, " :\n"); // get rid of string 'map'
}

void parse_table(table *t) {
  row *p = t->rows;
  int table_len = 0;
  char *tok = strtok(NULL, " :\n");
  while (NULL != tok && ('a' >= *tok || 'z' <= *tok)) {
    row r;
    r.dst = strtoll(tok, NULL, 10);
    tok = strtok(NULL, " :\n");
    r.src = strtoll(tok, NULL, 10);
    tok = strtok(NULL, " :\n");

    r.size = strtoll(tok, NULL, 10);
    *p = r;
    p++;
    table_len++;
    tok = strtok(NULL, " :\n");
  }
  t->len = table_len;
  if (NULL != tok) {
    tok = strtok(NULL, " :\n"); // get rid of string 'map'
  }
}

void parse_input(char *input, seeds *seeds, table *tables) {
  parse_seeds(input, seeds);
  puts("seeds:");
  for (int i = 0; i < seeds->len; i++) {
    printf("%lld ", seeds->seed[i]);
  }
  printf("\n");

  for (int i = 0; i < NTABLES; i++) {
    table *t = tables + i;
    parse_table(t);
  }

  puts("tables:");
  for (int i = 0; i < NTABLES; i++) {
    printf("table %d:\n", i);
    print_table(&tables[i]);
  }
}

int64_t solve(const seeds seeds, const table *tables) {
  int64_t res = LLONG_MAX;
  for (int i = 0; i < seeds.len; i += 2) {
    printf("Solving seed range %d\n", i);
    int64_t start = seeds.seed[i];
    int64_t end = start + seeds.seed[i + 1];
    for (uint64_t seed = start; seed < end; seed++) {
      int64_t mapped_val = seed;
      for (int j = 0; j < NTABLES; j++) {
        for (int64_t k = 0; k < tables[j].len; k++) {
          row r = tables[j].rows[k];
          if (mapped_val >= r.src && mapped_val < (r.src + r.size)) {
            mapped_val = (mapped_val - r.src) + r.dst;
            break;
          }
        }
      }
      if (mapped_val < res) {
        res = mapped_val;
      }
    }
  }
  return res;
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
  char *fname = "./sample.txt";
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

  seeds seeds;
  table tables[NTABLES];
  parse_input(input_txt, &seeds, tables);

  int64_t solution = solve(seeds, tables);
  printf("solution: %lld\n", solution);

  return EXIT_SUCCESS;
}
