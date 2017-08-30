; ModuleID = 'examplels.c'
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

; Function Attrs: nounwind uwtable
define i32 @ls(i32* %a, i32 %l, i32 %u, i32 %e) #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32*, align 8
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %i = alloca i32, align 4
  store i32* %a, i32** %2, align 8
  store i32 %l, i32* %3, align 4
  store i32 %u, i32* %4, align 4
  store i32 %e, i32* %5, align 4
  %6 = load i32* %3, align 4
  store i32 %6, i32* %i, align 4
  br label %7

; <label>:7                                       ; preds = %21, %0
  %8 = load i32* %i, align 4
  %9 = load i32* %4, align 4
  %10 = icmp sle i32 %8, %9
  br i1 %10, label %11, label %24

; <label>:11                                      ; preds = %7
  %12 = load i32* %i, align 4
  %13 = sext i32 %12 to i64
  %14 = load i32** %2, align 8
  %15 = getelementptr inbounds i32* %14, i64 %13
  %16 = load i32* %15, align 4
  %17 = load i32* %5, align 4
  %18 = icmp eq i32 %16, %17
  br i1 %18, label %19, label %20

; <label>:19                                      ; preds = %11
  store i32 1, i32* %1
  br label %25

; <label>:20                                      ; preds = %11
  br label %21

; <label>:21                                      ; preds = %20
  %22 = load i32* %i, align 4
  %23 = add nsw i32 %22, 1
  store i32 %23, i32* %i, align 4
  br label %7

; <label>:24                                      ; preds = %7
  store i32 0, i32* %1
  br label %25

; <label>:25                                      ; preds = %24, %19
  %26 = load i32* %1
  ret i32 %26
}

attributes #0 = { nounwind uwtable "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.ident = !{!0}

!0 = metadata !{metadata !"Debian clang version 3.5.0-10 (tags/RELEASE_350/final) (based on LLVM 3.5.0)"}
