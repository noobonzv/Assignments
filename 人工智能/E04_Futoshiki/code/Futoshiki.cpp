#include <iostream>
#include <fstream>
#include <vector>
#include <map>


using namespace std;
#define N 9                         
int board[N][N] = {0};              
bool assigned[N][N] = {false};          // 记录某一个格子是否已被赋值

int num_of_constrains = 0;

// 限制条件，两个坐标，前者大于后者
struct constraint{
    // x1y1 > x2y2
    int x1,y1;
    int x2,y2;
};

// 坐标
struct coordinate{
    int x;
    int y;
    // 重载 < 是为了 map 排序
    bool operator < (const coordinate &a) const
    {
        // 必须保证每个不同
        return x*10 + y < a.x*10 + a.y;
    }
};

map<coordinate, vector<int> > domain;               // 每个格子的值域
vector<constraint> constraints;                     // 所有的限制条件


// 列检查，去除该列的格子的值域中 与 cur_value 值相同的值
bool col_test(int r, int c, int cur_value){
    for(int j = 0; j < N; j++){
        if(!assigned[j][c]){                        // 首先保证该点还没有赋值
            vector<int>::iterator it;
            coordinate test{j,c};                   // 生成坐标，查map来查值域
            for (it = domain[test].begin(); it != domain[test].end(); ){
                if(*it == cur_value){
                    domain[test].erase(it);         //后面元素前移
                    if(domain[test].size() == 0) return 0;
                }
                else{
                    it++;
                }
            }
        }
    }
    return 1;
}

// 行检查，去除该行的格子的值域中 与 cur_value 值相同的值
bool row_test(int r, int c, int cur_value){
    for(int j = 0; j < N; j++){
        if(!assigned[r][j]){
            vector<int>::iterator it;
            coordinate test{r,j};                   //生成坐标
            for (it = domain[test].begin(); it != domain[test].end(); ){
                if(*it == cur_value){
                    domain[test].erase(it);         //后面元素前移
                    if(domain[test].size() == 0) return 0;
                }
                else{
                    it++;
                }
            }
            
        }
    }
    return 1;
}

// 限制条件的检查， 输入的坐标是应该较大的那个格子的坐标
bool constraint_test1(int x, int y, int value){
    coordinate test{x,y};
    vector<int>::iterator it;
    for (it = domain[test].begin(); it != domain[test].end(); ){
        if(value <= *it){                       // cur_vlaue 要大于后面的，所以删除大的
            domain[test].erase(it);             //后面元素前移
            if(domain[test].size() == 0) return 0;
        }
        else{
            it++;
        }
    }
    return 1;
}

// 限制条件的检查， 输入的坐标是应该较小的那个格子的坐标
bool constraint_test2(int x, int y, int value){
    coordinate test{x,y};
    vector<int>::iterator it;
    for (it = domain[test].begin(); it != domain[test].end(); ){
        if(value >= *it){                   // cur_vlaue 要大于后面的，所以删除大的
            domain[test].erase(it);             //后面元素前移
            if(domain[test].size() == 0) return 0;
        }
        else{
            it++;
        }
    }
    return 1;
}

// 读文件生成最初的board，并对部分值域做初步限制
int read_board(string filename){
    ifstream data;
    int r = 0, c = 0, num =0; 
    int n = 0;
    data.open(filename);
    while(!data.eof()){
        data >> r >> c >> num;
        // 最右一行可能，重复，由于eof的原因 !!!!!!!
        if(data.fail()) break;        // 如果碰到EOF，则failbit被设置为1，因此fin.fail()返回true
        //cout<<r<<c<<num<<endl;
        r--;          // 转换为数组下标
        c--;          
        assigned[r][c] = true;
        board[r][c] = num;
        n++;
       
        // 行检查
        bool test_row = row_test(r,c,num);
    
        // 列检测
        bool test_col = col_test(r,c,num);
    }

    data.close();
    return n;
}

// 读取大于小于限制条件， 并保存到一个vector中
void read_constraints(string filename, vector<constraint> & v){
    ifstream data;
    int x1,y1,x2,y2;
    data.open(filename);
    while(!data.eof()){
        data >> x1 >> y1 >> x2 >> y2;
         // 最右一行可能，重复，由于eof的原因 !!!!!!!
        if(data.fail()) break;        // 如果碰到EOF，则failbit被设置为1，因此fin.fail()返回true
        //cout<<r<<c<<num<<endl;
        x1--;          // 转换为数组下标
        y1--;
        x2--;
        y2--;   
        constraint c{x1,y1,x2,y2};      
        v.push_back(c);
        // 如果x1，y1已经取值而x2，y2还未取值
        if( (assigned[x1][y1]) && (!assigned[x2][y2]) ){      
           bool t = constraint_test1(x2,y2,board[x1][y1]);
        }
         // 如果x2，y2已经取值而x1，y1还未取值
        if( (assigned[x2][y2]) && (!assigned[x1][y1]) ){
            bool t = constraint_test2(x1,y1,board[x2][y2]);
        }

    }
    num_of_constrains = v.size();
    data.close();
}

// 输出board
void print_board(){
    for(int i = 0; i < N; i++){
        for(int j = 0; j < N; j++){
            cout << board[i][j] << " ";
        }
        cout << endl;
    }
}

// 判断是否找出答案
bool is_solved(){
    int n = 0;
    for(int i = 0; i < N; i++){
        for(int j = 0; j < N; j++){
            if(assigned[i][j]) n++;
        }
    }
    if(n == N*N) return true;
    else return false;
}

// 输出每个格子的值域， debug用
void print_domain(map<coordinate, vector<int> > domain_n){
    for(int i = 0; i < N; i++){
        for(int j = 0; j < N; j++){
            coordinate c{i,j};
            int len = domain_n[c].size();
            cout<<"["<<i<<","<<j<<"]"<<":";
            for(int k = 0; k < len; k++){
                cout<<domain_n[c][k]<<" ";
            }
            cout<<endl;
        }
    }
}

// 输出所有格子是否被赋值， debug用
void print_assigned(){
    for(int i = 0; i < N; i++){
        cout<<"*";
        for(int j = 0; j < N; j++){
           cout<<assigned[i][j]<<" ";
        }
        cout<<endl;
    }
}


// 用MRV来选择下一个赋值的格子，返回其坐标
coordinate MRV(){
    int min_i = 0, min_j =0, min = 9999;
    for(int i = 0; i < N; i++){
        for(int j = 0; j < N; j++){
            if(!assigned[i][j]){                //  首先是要未确定的点   
                coordinate c{i,j};
                int num = domain[c].size();     // 可取值的数的个数最少
                if(num < min ){
                    min = num;
                    min_i = i;
                    min_j = j;
                }
            }
        }
    }
    coordinate min_domain{min_i,min_j};
    return min_domain;
}

// 向前检查，去掉不和要求的取值
bool FCCheck(coordinate now, int cur_value){
    bool satisfied = true;
    int r = now.x;
    int c = now.y;
     // 行检查
    bool test_row = row_test(r,c,cur_value);
    if(!test_row) return false;
    // 同列检测
    bool test_col = col_test(r,c,cur_value);
    if(!test_col) return false;
    // 限制条件检查
    for(int j = 0; j < num_of_constrains; j++){
        int x1 = constraints[j].x1;
        int y1 = constraints[j].y1;
        int x2 = constraints[j].x2;
        int y2 = constraints[j].y2;
        bool t = true;
        if(x1 == now.x && y1 == now.y && (!assigned[x2][y2])){     
            t = constraint_test1(x2,y2,cur_value);
        }
        if(!t) return false;
        if(x2 == now.x && y2 == now.y && (!assigned[x1][y1])){
            t = constraint_test2(x1,y1,cur_value);
        }
        if(!t) return false;

    }
    return true;        //有值满足
}



void FC(){
    if(is_solved()){
        print_board();
        return;
    }
    coordinate now = MRV();                 // 得到下一个赋值的格子坐标
    map<coordinate, vector<int> > domain_copy = domain;      // 暂存目前所有格子的值域
    assigned[now.x][now.y] = true;
    int temp = board[now.y][now.y];
    vector<int> curDom = domain[now];
    int len = curDom.size();
    for(int i = 0; i < len; i++){
        domain = domain_copy;               // 每次对本格子赋值时都要恢复值域
        board[now.x][now.y] = curDom[i];
        bool exist_satisfy_all = FCCheck(now, curDom[i]);
        if(!exist_satisfy_all){
            board[now.y][now.y] = temp;
            continue;
        }
        else{
            FC();
        }
    }
    assigned[now.x][now.y] = false;         // 回复未赋值状态
    return;

}



int main(){
    int num_assigned = 0;
    vector<int> domain_of_each_tile;
    // 每个格子初始值域 1-9
    for(int i = 1; i <= N; i++) {
        domain_of_each_tile.push_back(i);
    }
    for(int i = 0; i < N; i++){
        for(int j = 0; j < N; j++){
            coordinate c{i,j};
            domain[c] = domain_of_each_tile;
        }
    }

    num_assigned = read_board("board.txt");
    read_constraints("constraint.txt", constraints);
    FC();
}
