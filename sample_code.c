
#include <stdio.h>
#include <stdlib.h>

// 计算阶乘的函数
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

// 主函数
int main() {
    int num = 5;
    int result;
    
    printf("计算 %d 的阶乘\n", num);
    result = factorial(num);
    printf("%d! = %d\n", num, result);
    
    return 0;
}
