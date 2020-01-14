import pickle

####generate prime
def seive(dic,N):
    p=2
    while p*p<=N:
        if dic[p]==True:
            for j in range(p*p,N+1,p):
                dic[j]=False
        p+=1
    return dic

if __name__=='__main__':
    N=100000
    dic={}
    for i in range(2,N+1):
        dic[i]=True
    dic=seive(dic,N)
    primes=[]
    for d in dic:
        if dic[d]==True:
            primes.append(d)
    with open('C:\\Users\\tusha\Desktop\\Neuro-Evolutionary model\\FLAPPY BIRDS\prime_list.pkl','wb') as f:
        pickle.dump(primes,f)
    f.close()
