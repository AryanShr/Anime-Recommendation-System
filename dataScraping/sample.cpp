#include <bits/stdc++.h>
using namespace std;

bool solve(vector<int>&arr, int n){
    int d = arr[1]-arr[0];
	for(int i = 2;i<n;i++){
	    if(d != (arr[i]- arr[i-1])) return false;
	 }
	 return true;
}

int main() {
	// your code goes here
	int t;
	cin>>t;
	while(t--){
	    int n;
	    cin>>n;
	    vector<int>arr;
	    for(int i = 0 ;i<n;i++)cin>>arr[i];
	    if(solve(arr,n)){
	        cout<<"Yes"<<endl;
	    }
	    else cout<<"No"<<endl;
	}
	return 0;
}
