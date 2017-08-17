#!/bin/bash

choose_type()
{
	tip1="
choose type(1-9):
	1. <feat>: 新增feature
	2. <fix>: 修复bug
	3. <docs>: 仅仅修改了文档，比如README, CHANGELOG, CONTRIBUTE等等
	4. <style>: 仅仅修改了空格、格式缩进、都好等等，不改变代码逻辑
	5. <refactor>: 代码重构，没有加新功能或者修复bug
	6. <perf>: 优化相关，比如提升性能、体验
	7. <test>: 测试用例，包括单元测试、集成测试等
	8. <chore>: 改变构建流程、或者增加依赖库、工具等
	9. <revert>: 回滚到上一个版本

	"
	echo "----------------------------------------"
	echo "$tip1"

	while true
	do
		read type_num
		case "$type_num" in
			"1" )
				type_m="feat"
				break;;
			"2" )
				type_m="fix"
				break;;
			"3" )
				type_m="docs"
				break;;
			"4" )
				type_m="style"
				break;;
			"5" )
				type_m="refactor"
				break;;
			"6" )
				type_m="perf"
				break;;
			"7" )
				type_m="test"
				break;;
			"8" )
				type_m="chore"
				break;;
			"9" )
				type_m="revert"
				break;;
			* )
				echo "error type！re-select";;
		esac
	done
}

edit_scope()
{
	echo "----------------------------------------"
	echo -e "input the scope (<file name> or <*>):"
	read scope
}

edit_subject()
{
	echo "----------------------------------------"
	echo -e "input the subject (describe the changes):"
	read subject
}



edit_commit_message()
{
	echo "edit commit message..."

	while true
	do
		choose_type
		echo "----------------------------------------"
		echo "you have chosen type $type_num : $type_m"
		echo "go on? (y/n):[y] "
		read key1
		if [ $key1=='y' ] || [ $key1=='' ]
		then
			break
		fi
	done


	while true
	do
		edit_scope
		echo "----------------------------------------"
		echo -e "your scope is: \n $scope"
		echo "go on? (y/n)[y]: "
		read key2
		if [ $key2=='y' ] || [ $key2=='' ]
		then
			break
		fi
	done


	while true
	do
		edit_subject
		echo "----------------------------------------"
		echo -e "your subject is: \n $subject"
		echo "go on? (y/n)[y]: "
		read key3
		if [ $key3=='y' ] || [ $key3=='' ]
		then
			break
		fi
	done
	
	message="$type_m($scope): $subject"
}


echo "*********************************************************"

#echo "jekyll build..."
#bundle exec jekyll build
#echo "build done"

#echo "*********************************************************"

echo "git add ..."
git add .
echo "add done"

echo -e "\n*********************************************************"

while true
do
	edit_commit_message
	echo "========================================"
	echo -e "your message is: \n $message"
	echo "go on? (y/n): "
	read key4
	if [ $key4=='y' ]
	then
		break
	fi
done

echo "----------------------------------------"
echo "edit message done"

echo "*********************************************************"

echo "git commit ..."
git commit -m "$message"
echo "commit done"

echo "*********************************************************"

echo "git push ..."
git push origin master
echo "push done"

echo "*********************************************************"

echo "completed"
