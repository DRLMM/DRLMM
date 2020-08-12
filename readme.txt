Little Yueyue is comming!

Welcome to our team -- DRLMM!

1. 初始化一个Git仓库，使用git init命令

2.  添加文件到git仓库，分两步：
	1）使用命令git add <file>，注意，可反复多次使用，添加多个文件；
	2）使用命令git commit -m <message> 完成
	
3. git status命令可以让我们时刻掌握仓库当前的状态，哪些文件被修改过，但是还没有准备提交

4. git diff <file> 可以查看有哪些不同呢？

5. HEAD指向的版本就是当前版本，因此，GIT允许我们在版本的历史之间穿梭，使用命令git reset --hard commit_id 或者HEAD^^ HEAD~100

6.穿梭前，用git log可以查看提交历史，以便确定要回退到哪个版本。

7. 要重返未来，用git reflog查看命令历史，以便确定要回到未来的哪个版本。

8. 当远程分支上存在本地分支中不存在的提交，往往是多人协作开发过程中遇到的问题，可以先fetch再merge,也就是pull，再把远程分支上
的提交合并到本地分支之后再push,也可以强行让本地分支覆盖远程分支，git push origin master -f

9. 先git pull origin master --allow-unrelated-histories  再git push origin master

要关联一个远程库，使用命令git remote add origin git@server-name:path/repo-name.git；

关联后，使用命令git push -u origin master第一次推送master分支的所有内容；

此后，每次本地提交后，只要有必要，就可以使用命令git push origin master推送最新修改；