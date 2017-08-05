#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int prime(int n) {
	for (int i = 0; i * i <= n; i++) {
		if (n % i == 0) {
			return 1;
		}
	}
	return 0;
}
