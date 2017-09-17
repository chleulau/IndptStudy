; ModuleID = 'examplels2.c'
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@.str = private unnamed_addr constant [7 x i8] c"l <= i\00", align 1
@.str1 = private unnamed_addr constant [13 x i8] c"examplels2.c\00", align 1
@__PRETTY_FUNCTION__.ls = private unnamed_addr constant [29 x i8] c"int ls(int *, int, int, int)\00", align 1
@.str2 = private unnamed_addr constant [7 x i8] c"i <= u\00", align 1

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

; <label>:7                                       ; preds = %35, %0
  %8 = load i32* %i, align 4
  %9 = load i32* %4, align 4
  %10 = icmp sle i32 %8, %9
  br i1 %10, label %11, label %38

; <label>:11                                      ; preds = %7
  %12 = load i32* %3, align 4
  %13 = load i32* %i, align 4
  %14 = icmp sle i32 %12, %13
  br i1 %14, label %15, label %16

; <label>:15                                      ; preds = %11
  br label %18

; <label>:16                                      ; preds = %11
  call void @__assert_fail(i8* getelementptr inbounds ([7 x i8]* @.str, i32 0, i32 0), i8* getelementptr inbounds ([13 x i8]* @.str1, i32 0, i32 0), i32 9, i8* getelementptr inbounds ([29 x i8]* @__PRETTY_FUNCTION__.ls, i32 0, i32 0)) #2
  unreachable
                                                  ; No predecessors!
  br label %18

; <label>:18                                      ; preds = %17, %15
  %19 = load i32* %i, align 4
  %20 = sext i32 %19 to i64
  %21 = load i32** %2, align 8
  %22 = getelementptr inbounds i32* %21, i64 %20
  %23 = load i32* %22, align 4
  %24 = load i32* %5, align 4
  %25 = icmp eq i32 %23, %24
  br i1 %25, label %26, label %34

; <label>:26                                      ; preds = %18
  %27 = load i32* %i, align 4
  %28 = load i32* %4, align 4
  %29 = icmp sle i32 %27, %28
  br i1 %29, label %30, label %31

; <label>:30                                      ; preds = %26
  br label %33

; <label>:31                                      ; preds = %26
  call void @__assert_fail(i8* getelementptr inbounds ([7 x i8]* @.str2, i32 0, i32 0), i8* getelementptr inbounds ([13 x i8]* @.str1, i32 0, i32 0), i32 11, i8* getelementptr inbounds ([29 x i8]* @__PRETTY_FUNCTION__.ls, i32 0, i32 0)) #2
  unreachable
                                                  ; No predecessors!
  br label %33

; <label>:33                                      ; preds = %32, %30
  store i32 1, i32* %1
  br label %39

; <label>:34                                      ; preds = %18
  br label %35

; <label>:35                                      ; preds = %34
  %36 = load i32* %i, align 4
  %37 = add nsw i32 %36, 1
  store i32 %37, i32* %i, align 4
  br label %7

; <label>:38                                      ; preds = %7
  store i32 0, i32* %1
  br label %39

; <label>:39                                      ; preds = %38, %33
  %40 = load i32* %1
  ret i32 %40
}

; Function Attrs: noreturn nounwind
declare void @__assert_fail(i8*, i8*, i32, i8*) #1

attributes #0 = { nounwind uwtable "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { noreturn nounwind "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { noreturn nounwind }

!llvm.ident = !{!0}

!0 = metadata !{metadata !"Debian clang version 3.5.0-10 (tags/RELEASE_350/final) (based on LLVM 3.5.0)"}
