#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <sys/stat.h>

#define TABLE_CAP 100
#define NTABLES 7
#define MAX_SEEDS_N 100

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

void print_row(row r) { printf("%lld, %lld, %lld\n", r.dst, r.src, r.size); }
void print_table(table t) {
  for (int i = 0; i < t.len; i++) {
    print_row(t.rows[i]);
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

  char ftxt[input_st.st_size + 1];

  FILE *inputf = fopen(fname, "rb");
  if (!inputf) {
    printf("Couldn't open file %s\n", fname);
    exit(EXIT_FAILURE);
  }

  if (-1 == fread(ftxt, 1, input_st.st_size, inputf)) {
    printf("error reading file %s", fname);
    perror("Error");
    exit(EXIT_FAILURE);
  }
  ftxt[input_st.st_size] = '\0';
  char *fparse = ftxt;
  seeds seeds;
  parse_seeds(fparse, &seeds);
  puts("seeds:");
  for (int i = 0; i < seeds.len; i++) {
    printf("%lld ", seeds.seed[i]);
  }
  printf("\n");

  table tables[NTABLES];
  for (int i = 0; i < NTABLES; i++) {
    table *t = tables + i;
    parse_table(t);
  }

  puts("tables:");
  for (int i = 0; i < NTABLES; i++) {
    printf("table %d:\n", i);
    print_table(tables[i]);
  }

  int64_t solution = solve(seeds, tables);
  printf("solution: %lld\n", solution);

  fclose(inputf);
  return EXIT_SUCCESS;
}
