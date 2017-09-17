//Hypothetically, e is the integer square root of n

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

int notprime(int n, int e) {
	int i;
	for (i = 2; i <= e; i++) {
		assert(i <= e);
		if (n % i == 0) {
			return 1;
		}
	}
	return 0;
}
