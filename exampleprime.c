//Hypothetically, e is the integer square root of n

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int notprime(int n, int e) {
	for (int i = 2; i <= e; i++) {
		if (n % i == 0) {
			return 1;
		}
	}
	return 0;
}
