#include <limits.h>
#include <pthread.h>
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

typedef struct work {
  int64_t start;
  int64_t stop;
  int64_t res;
  table *tables;
} work;

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
    print_table(tables[i]);
  }
}

void *solver(void *w) {
  work *work = w;
  int64_t res = LLONG_MAX;
  printf("starting work \n");
  for (uint64_t seed = work->start; seed < work->stop; seed++) {
    int64_t mapped_val = seed;
    for (int j = 0; j < NTABLES; j++) {
      for (int k = 0; k < work->tables[j].len; k++) {
        row r = work->tables[j].rows[k];
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

  printf("finishing work \n");
  work->res = res;
  return NULL;
}

void read_file(char *fname, char *ret_txt, size_t fsize, size_t strsize) {
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

  read_file(fname, input_txt, input_st.st_size, txtsize);

  seeds seeds;
  table tables[NTABLES];
  parse_input(input_txt, &seeds, tables);

  int num_ranges = seeds.len / 2;

  work todo[num_ranges];
  pthread_t ts[num_ranges];
  for (int i = 0; i < seeds.len; i += 2) {
    work w;
    w.start = seeds.seed[i];
    w.stop = seeds.seed[i + 1] + w.start;
    w.tables = tables;
    todo[i / 2] = w;
    pthread_create(&ts[i / 2], NULL, solver, (void *)&todo[i / 2]);
  }

  for (int i = 0; i < seeds.len / 2; i++) {
    pthread_join(ts[i], NULL);
  }

  int64_t solution = todo[0].res;
  for (int i = 1; i < num_ranges; i++) {
    if (todo[i].res < solution) {
      solution = todo[i].res;
    }
  }

  printf("solution: %lld\n", solution);

  return EXIT_SUCCESS;
}
