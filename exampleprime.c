#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int notprime(int n) {
	for (int i = 2; i * i <= n; i++) {
		if (n % i == 0) {
			return 1;
		}
	}
	return 0;
}
