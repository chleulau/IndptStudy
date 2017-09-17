; ModuleID = 'exampleps1.c'
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@.str = private unnamed_addr constant [7 x i8] c"i <= e\00", align 1
@.str1 = private unnamed_addr constant [13 x i8] c"exampleps1.c\00", align 1
@__PRETTY_FUNCTION__.notprime = private unnamed_addr constant [23 x i8] c"int notprime(int, int)\00", align 1

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

; <label>:4                                       ; preds = %22, %0
  %5 = load i32* %i, align 4
  %6 = load i32* %3, align 4
  %7 = icmp sle i32 %5, %6
  br i1 %7, label %8, label %25

; <label>:8                                       ; preds = %4
  %9 = load i32* %i, align 4
  %10 = load i32* %3, align 4
  %11 = icmp sle i32 %9, %10
  br i1 %11, label %12, label %13

; <label>:12                                      ; preds = %8
  br label %15

; <label>:13                                      ; preds = %8
  call void @__assert_fail(i8* getelementptr inbounds ([7 x i8]* @.str, i32 0, i32 0), i8* getelementptr inbounds ([13 x i8]* @.str1, i32 0, i32 0), i32 11, i8* getelementptr inbounds ([23 x i8]* @__PRETTY_FUNCTION__.notprime, i32 0, i32 0)) #2
  unreachable
                                                  ; No predecessors!
  br label %15

; <label>:15                                      ; preds = %14, %12
  %16 = load i32* %2, align 4
  %17 = load i32* %i, align 4
  %18 = srem i32 %16, %17
  %19 = icmp eq i32 %18, 0
  br i1 %19, label %20, label %21

; <label>:20                                      ; preds = %15
  store i32 1, i32* %1
  br label %26

; <label>:21                                      ; preds = %15
  br label %22

; <label>:22                                      ; preds = %21
  %23 = load i32* %i, align 4
  %24 = add nsw i32 %23, 1
  store i32 %24, i32* %i, align 4
  br label %4

; <label>:25                                      ; preds = %4
  store i32 0, i32* %1
  br label %26

; <label>:26                                      ; preds = %25, %20
  %27 = load i32* %1
  ret i32 %27
}

; Function Attrs: noreturn nounwind
declare void @__assert_fail(i8*, i8*, i32, i8*) #1

attributes #0 = { nounwind uwtable "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { noreturn nounwind "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { noreturn nounwind }

!llvm.ident = !{!0}

!0 = metadata !{metadata !"Debian clang version 3.5.0-10 (tags/RELEASE_350/final) (based on LLVM 3.5.0)"}
