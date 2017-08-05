; ModuleID = 'exampleprime.c'
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

; Function Attrs: nounwind uwtable
define i32 @prime(i32 %n) #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %i = alloca i32, align 4
  store i32 %n, i32* %2, align 4
  store i32 0, i32* %i, align 4
  br label %3

; <label>:3                                       ; preds = %16, %0
  %4 = load i32* %i, align 4
  %5 = load i32* %i, align 4
  %6 = mul nsw i32 %4, %5
  %7 = load i32* %2, align 4
  %8 = icmp sle i32 %6, %7
  br i1 %8, label %9, label %19

; <label>:9                                       ; preds = %3
  %10 = load i32* %2, align 4
  %11 = load i32* %i, align 4
  %12 = srem i32 %10, %11
  %13 = icmp eq i32 %12, 0
  br i1 %13, label %14, label %15

; <label>:14                                      ; preds = %9
  store i32 1, i32* %1
  br label %20

; <label>:15                                      ; preds = %9
  br label %16

; <label>:16                                      ; preds = %15
  %17 = load i32* %i, align 4
  %18 = add nsw i32 %17, 1
  store i32 %18, i32* %i, align 4
  br label %3

; <label>:19                                      ; preds = %3
  store i32 0, i32* %1
  br label %20

; <label>:20                                      ; preds = %19, %14
  %21 = load i32* %1
  ret i32 %21
}

attributes #0 = { nounwind uwtable "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.ident = !{!0}

!0 = metadata !{metadata !"Debian clang version 3.5.0-10 (tags/RELEASE_350/final) (based on LLVM 3.5.0)"}
