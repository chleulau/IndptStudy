; ModuleID = 'examplebs.c'
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

; Function Attrs: nounwind uwtable
define i32 @bs(i32* %a, i32 %l, i32 %u, i32 %e) #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32*, align 8
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %m = alloca i32, align 4
  store i32* %a, i32** %2, align 8
  store i32 %l, i32* %3, align 4
  store i32 %u, i32* %4, align 4
  store i32 %e, i32* %5, align 4
  %6 = load i32* %3, align 4
  %7 = load i32* %4, align 4
  %8 = icmp sgt i32 %6, %7
  br i1 %8, label %9, label %10

; <label>:9                                       ; preds = %0
  store i32 0, i32* %1
  br label %45

; <label>:10                                      ; preds = %0
  %11 = load i32* %3, align 4
  %12 = load i32* %4, align 4
  %13 = add nsw i32 %11, %12
  %14 = sdiv i32 %13, 2
  store i32 %14, i32* %m, align 4
  %15 = load i32* %m, align 4
  %16 = sext i32 %15 to i64
  %17 = load i32** %2, align 8
  %18 = getelementptr inbounds i32* %17, i64 %16
  %19 = load i32* %18, align 4
  %20 = load i32* %5, align 4
  %21 = icmp eq i32 %19, %20
  br i1 %21, label %22, label %23

; <label>:22                                      ; preds = %10
  store i32 1, i32* %1
  br label %45

; <label>:23                                      ; preds = %10
  %24 = load i32* %m, align 4
  %25 = sext i32 %24 to i64
  %26 = load i32** %2, align 8
  %27 = getelementptr inbounds i32* %26, i64 %25
  %28 = load i32* %27, align 4
  %29 = load i32* %5, align 4
  %30 = icmp slt i32 %28, %29
  br i1 %30, label %31, label %38

; <label>:31                                      ; preds = %23
  %32 = load i32** %2, align 8
  %33 = load i32* %m, align 4
  %34 = add nsw i32 %33, 1
  %35 = load i32* %4, align 4
  %36 = load i32* %5, align 4
  %37 = call i32 @bs(i32* %32, i32 %34, i32 %35, i32 %36)
  store i32 %37, i32* %1
  br label %45

; <label>:38                                      ; preds = %23
  %39 = load i32** %2, align 8
  %40 = load i32* %3, align 4
  %41 = load i32* %m, align 4
  %42 = sub nsw i32 %41, 1
  %43 = load i32* %5, align 4
  %44 = call i32 @bs(i32* %39, i32 %40, i32 %42, i32 %43)
  store i32 %44, i32* %1
  br label %45

; <label>:45                                      ; preds = %38, %31, %22, %9
  %46 = load i32* %1
  ret i32 %46
}

attributes #0 = { nounwind uwtable "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.ident = !{!0}

!0 = metadata !{metadata !"Debian clang version 3.5.0-10 (tags/RELEASE_350/final) (based on LLVM 3.5.0)"}
