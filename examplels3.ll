; ModuleID = 'examplels3.c'
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@.str = private unnamed_addr constant [21 x i8] c"(l <= i) && (i <= u)\00", align 1
@.str1 = private unnamed_addr constant [13 x i8] c"examplels3.c\00", align 1
@__PRETTY_FUNCTION__.ls = private unnamed_addr constant [29 x i8] c"int ls(int *, int, int, int)\00", align 1

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

; <label>:7                                       ; preds = %32, %0
  %8 = load i32* %i, align 4
  %9 = load i32* %4, align 4
  %10 = icmp sle i32 %8, %9
  br i1 %10, label %11, label %35

; <label>:11                                      ; preds = %7
  %12 = load i32* %3, align 4
  %13 = load i32* %i, align 4
  %14 = icmp sle i32 %12, %13
  br i1 %14, label %15, label %20

; <label>:15                                      ; preds = %11
  %16 = load i32* %i, align 4
  %17 = load i32* %4, align 4
  %18 = icmp sle i32 %16, %17
  br i1 %18, label %19, label %20

; <label>:19                                      ; preds = %15
  br label %22

; <label>:20                                      ; preds = %15, %11
  call void @__assert_fail(i8* getelementptr inbounds ([21 x i8]* @.str, i32 0, i32 0), i8* getelementptr inbounds ([13 x i8]* @.str1, i32 0, i32 0), i32 9, i8* getelementptr inbounds ([29 x i8]* @__PRETTY_FUNCTION__.ls, i32 0, i32 0)) #2
  unreachable
                                                  ; No predecessors!
  br label %22

; <label>:22                                      ; preds = %21, %19
  %23 = load i32* %i, align 4
  %24 = sext i32 %23 to i64
  %25 = load i32** %2, align 8
  %26 = getelementptr inbounds i32* %25, i64 %24
  %27 = load i32* %26, align 4
  %28 = load i32* %5, align 4
  %29 = icmp eq i32 %27, %28
  br i1 %29, label %30, label %31

; <label>:30                                      ; preds = %22
  store i32 1, i32* %1
  br label %36

; <label>:31                                      ; preds = %22
  br label %32

; <label>:32                                      ; preds = %31
  %33 = load i32* %i, align 4
  %34 = add nsw i32 %33, 1
  store i32 %34, i32* %i, align 4
  br label %7

; <label>:35                                      ; preds = %7
  store i32 0, i32* %1
  br label %36

; <label>:36                                      ; preds = %35, %30
  %37 = load i32* %1
  ret i32 %37
}

; Function Attrs: noreturn nounwind
declare void @__assert_fail(i8*, i8*, i32, i8*) #1

attributes #0 = { nounwind uwtable "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { noreturn nounwind "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { noreturn nounwind }

!llvm.ident = !{!0}

!0 = metadata !{metadata !"Debian clang version 3.5.0-10 (tags/RELEASE_350/final) (based on LLVM 3.5.0)"}
