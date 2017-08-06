; ModuleID = 'exampleprime.c'
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

; Function Attrs: nounwind uwtable
define i32 @notprime(i32 %n, i32 %e) #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  %i = alloca i32, align 4
  store i32 %n, i32* %2, align 4
  store i32 %e, i32* %3, align 4
  store i32 2, i32* %i, align 4
  br label %4

; <label>:4                                       ; preds = %15, %0
  %5 = load i32* %i, align 4
  %6 = load i32* %3, align 4
  %7 = icmp sle i32 %5, %6
  br i1 %7, label %8, label %18

; <label>:8                                       ; preds = %4
  %9 = load i32* %2, align 4
  %10 = load i32* %i, align 4
  %11 = srem i32 %9, %10
  %12 = icmp eq i32 %11, 0
  br i1 %12, label %13, label %14

; <label>:13                                      ; preds = %8
  store i32 1, i32* %1
  br label %19

; <label>:14                                      ; preds = %8
  br label %15

; <label>:15                                      ; preds = %14
  %16 = load i32* %i, align 4
  %17 = add nsw i32 %16, 1
  store i32 %17, i32* %i, align 4
  br label %4

; <label>:18                                      ; preds = %4
  store i32 0, i32* %1
  br label %19

; <label>:19                                      ; preds = %18, %13
  %20 = load i32* %1
  ret i32 %20
}

attributes #0 = { nounwind uwtable "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.ident = !{!0}

!0 = metadata !{metadata !"Debian clang version 3.5.0-10 (tags/RELEASE_350/final) (based on LLVM 3.5.0)"}
