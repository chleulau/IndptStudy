#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int fib(int n) {
	int a = 0;
	int b = 1;
	for (int i = 0; i < n; i++) {
		int c = b;
		b = a + b;
		a = c;
	}
	return b;
}
