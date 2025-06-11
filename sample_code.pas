
program FactorialExample;

{ 计算阶乘的函数 }
function Factorial(n: integer): integer;
begin
    if n <= 1 then
        Factorial := 1
    else
        Factorial := n * Factorial(n - 1);
end;

{ 主程序 }
var
    num, result: integer;
begin
    num := 5;
    writeln('计算 ', num, ' 的阶乘');
    result := Factorial(num);
    writeln(num, '! = ', result);
end.
