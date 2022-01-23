% Use this editor as a MiniZinc scratch book
int: no_servers; %l. serwerów
int: no_users; %l. użytkowników
int: no_contents; % l. rodzajów treści


%array declaration
%sets
set of int: SERVERS = 1..no_servers;
set of int: USERS = 1..no_users;
set of int: CONTENTS = 1..no_contents;

%arrays
%inputs
array[SERVERS] of int: capacity;
array[SERVERS] of int: x_server;
array[SERVERS] of int: y_server;

array[CONTENTS] of int: content_size;

array[USERS] of int: x_user;
array[USERS] of int: y_user;
array[USERS,CONTENTS] of bool: matrix_interest;
%end of inputs
%function
function float: calculate(int:x1, int: y1,  int: x2,  int: y2) = sqrt(pow(x1-x2,2)+pow(y1-y2,2));

function var float: cost()=sum(u in USERS,i in CONTENTS, j in SERVERS)(distances_orch_servers[j]*content_size[i]+bool2int(use_server[u,j,i])*5+bool2int(use_server[u,i,j])*content_size[i]*distances_user_server[u,j]) ;
%helpful variables
array[int] of float: distances_orch_servers= [sqrt(pow(x_server[i],2)+pow(y_server[i],2)) | i in SERVERS];

array[int,int] of float: distances_user_server=array2d(USERS,SERVERS, [calculate(x_server[i], y_server[i], x_user[j], y_user[j]) | i in SERVERS, j in USERS]);


% zmienne decyzyjne

array[CONTENTS, SERVERS] of var bool: content_on_server;
array[USERS,CONTENTS,SERVERS] of var bool: use_server;

% constraints

constraint 
  forall(i in SERVERS) (
    sum(j in CONTENTS)(bool2int(content_on_server[j,i])*content_size[j]) <= capacity[i]
  );
constraint %żeby nie zwracało samych 0
sum(i in SERVERS, j in CONTENTS)(content_on_server[j,i]) >0;
constraint
  forall(u in USERS) (
  sum(i in SERVERS,j in CONTENTS)(bool2int(use_server[u,j,i])) == sum(i in CONTENTS)(bool2int(matrix_interest[u,i])));

constraint
  sum(i in SERVERS,j in CONTENTS)(bool2int(content_on_server[j,i])) == sum(i in SERVERS, u in USERS, j in CONTENTS)(bool2int(use_server[u,j,i]));
   
  
% rozwiąż- funkcja celu
solve minimize cost();

output [ "Contents on server: \(s) = \(content_on_server[CONTENTS, s]);\n" | s in SERVERS ]