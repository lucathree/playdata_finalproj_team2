lrate="1 0.1 0.01 0.001"

for ((e=1; e<=3; e++))
do
	for ((b=1; b<=6; b++))
	do
		for lr in $lrate
		do
			python /home/ubuntu/aiml/lane_model/src_test/train.py -e=$e -b=$b -lr=$lr
		done
	done
done