
def solution(A):
	
	if len(A)%2 == 1:
		return False

	dict = {}
	for val in A:
		# print(dict)
		if val in dict:
			del dict[val]
		else:
			dict[val] = 1

	if len(dict)>0:
		return False

	return True

A = [1,2,2,1]
B = [7,7,7]
C = [1,2,2,3]
print(solution(A))
print(solution(B))
print(solution(C))