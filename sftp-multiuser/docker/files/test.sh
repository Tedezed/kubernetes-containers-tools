LIST_USERS='ted=tedpass bob=bobpass'
USER_UID=1000
for user in ${LIST_USERS[@]}
do
	array=(${user//=/ }) # split
	echo $USER_UID
	echo ${array[0]}
	echo ${array[1]}
	USER_UID=$((USER_UID+1))
done