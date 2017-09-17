#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

int ls(int* a, int l, int u, int e) {
	int i;
	for (i = l; i <= u; i++) {
		assert(l <= i);
		if (a[i] == e) {
			assert(i <= u);
			return 1;
		}
	}
	return 0;
}
