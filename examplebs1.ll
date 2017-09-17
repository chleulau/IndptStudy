; ModuleID = 'examplebs1.c'
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@.str = private unnamed_addr constant [7 x i8] c"l <= u\00", align 1
@.str1 = private unnamed_addr constant [13 x i8] c"examplebs1.c\00", align 1
@__PRETTY_FUNCTION__.bs = private unnamed_addr constant [29 x i8] c"int bs(int *, int, int, int)\00", align 1

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
  br label %52

; <label>:10                                      ; preds = %0
  %11 = load i32* %3, align 4
  %12 = load i32* %4, align 4
  %13 = add nsw i32 %11, %12
  %14 = sdiv i32 %13, 2
  store i32 %14, i32* %m, align 4
  %15 = load i32* %3, align 4
  %16 = load i32* %4, align 4
  %17 = icmp sle i32 %15, %16
  br i1 %17, label %18, label %19

; <label>:18                                      ; preds = %10
  br label %21

; <label>:19                                      ; preds = %10
  call void @__assert_fail(i8* getelementptr inbounds ([7 x i8]* @.str, i32 0, i32 0), i8* getelementptr inbounds ([13 x i8]* @.str1, i32 0, i32 0), i32 10, i8* getelementptr inbounds ([29 x i8]* @__PRETTY_FUNCTION__.bs, i32 0, i32 0)) #2
  unreachable
                                                  ; No predecessors!
  br label %21

; <label>:21                                      ; preds = %20, %18
  %22 = load i32* %m, align 4
  %23 = sext i32 %22 to i64
  %24 = load i32** %2, align 8
  %25 = getelementptr inbounds i32* %24, i64 %23
  %26 = load i32* %25, align 4
  %27 = load i32* %5, align 4
  %28 = icmp eq i32 %26, %27
  br i1 %28, label %29, label %30

; <label>:29                                      ; preds = %21
  store i32 1, i32* %1
  br label %52

; <label>:30                                      ; preds = %21
  %31 = load i32* %m, align 4
  %32 = sext i32 %31 to i64
  %33 = load i32** %2, align 8
  %34 = getelementptr inbounds i32* %33, i64 %32
  %35 = load i32* %34, align 4
  %36 = load i32* %5, align 4
  %37 = icmp slt i32 %35, %36
  br i1 %37, label %38, label %45

; <label>:38                                      ; preds = %30
  %39 = load i32** %2, align 8
  %40 = load i32* %m, align 4
  %41 = add nsw i32 %40, 1
  %42 = load i32* %4, align 4
  %43 = load i32* %5, align 4
  %44 = call i32 @bs(i32* %39, i32 %41, i32 %42, i32 %43)
  store i32 %44, i32* %1
  br label %52

; <label>:45                                      ; preds = %30
  %46 = load i32** %2, align 8
  %47 = load i32* %3, align 4
  %48 = load i32* %m, align 4
  %49 = sub nsw i32 %48, 1
  %50 = load i32* %5, align 4
  %51 = call i32 @bs(i32* %46, i32 %47, i32 %49, i32 %50)
  store i32 %51, i32* %1
  br label %52

; <label>:52                                      ; preds = %45, %38, %29, %9
  %53 = load i32* %1
  ret i32 %53
}

; Function Attrs: noreturn nounwind
declare void @__assert_fail(i8*, i8*, i32, i8*) #1

attributes #0 = { nounwind uwtable "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { noreturn nounwind "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { noreturn nounwind }

!llvm.ident = !{!0}

!0 = metadata !{metadata !"Debian clang version 3.5.0-10 (tags/RELEASE_350/final) (based on LLVM 3.5.0)"}
