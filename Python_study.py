## format
'''
print('{} {}'.format('one','two'))
print('{} {}'.format(123, 450))
print('{1} {0}'.format('one','two'))
print('{:10.5}'.format('pythonstudy')) # 10자리의 자릿수 중에서 5개만 보여줌

tuple = (1,2,3)
set = {1,2,3} # or 1,2,3
dict = {"123":123}
'''

## naming
'''
camel case : numberOfCollegeGraduates -> Method
Pascal case : NumberOfCollegeGraduates -> Class
Snake case : number_of_college_graduates -> 변수(파이썬에서 자주 사용)
'''

## 연산
'''
pow(2,3) = 2 ** 3 (2의 3제곱)
a = [1,2,3]
print(a.pop()) = 3 (a = [1,2] / 마지막 원소 제거 )
a.count(3) = 1
a.count("사과") = ??
a.extend([4,5]) / a = [1,2,3,4,5] (원소 추가)
'''

## 자료형
'''
# 튜플 (순서 o, 중복 o, 수정 x, 삭제 x) # 불변 & 나머지는 다 똑같음
a = (1,2,3)
b = list(a)
unpacking
(x1,x2,x3) = a

packing
x1,x2,x3 = [1,2,3]
c = (x1,x2,x3)

# dict (순서 x, 중복 x, 수정 o, 삭제 o)
tuple in dict도 가능함

dict 추가 
a = dict(
    'a' = 1,
    'b' = 2
)
a['c']=3

a.keys & a.values & a.items(key, value를 tuple형태로 가져옴) & a.pop('a') ..
a.update(a='123')

# set (순서 x, 중복 x, 수정 o, 삭제 o)
a = set()
b = set([1,2,3]) or b = {1,2,3}
c = tuple(b) or c = list(b) # 튜플이나 리스트로 전환 가능
'''




