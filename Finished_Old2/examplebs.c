#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int bs(int* a, int l, int u, int e) {
	if (l > u) {return 0;}
	else {
		int m = (l + u) / 2;
		if (a[m] == e) {
			return 1;
		} else {
			if (a[m] < e) {
				return bs(a, m + 1, u, e);
			} else {
				return bs(a, l, m - 1, e);
			}
		}
	}
}
