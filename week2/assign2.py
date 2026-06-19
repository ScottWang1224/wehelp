# =========TASK1===========
def func1(name): 
     # 定位各角色
     positions = {
          "悟空":(0,0),
          "辛巴":(-3,3),
          "丁滿":(-1,4),
          "⾙吉塔":(-4,-1),
          "特南克斯":(1,-2),
          "弗利沙":(4,-1)
     }
     sides = {
    "悟空": "left",
    "辛巴": "left",
    "⾙吉塔": "left",
    "特南克斯": "left",
    "弗利沙": "right",
    "丁滿": "right"
     }
     farthest_names = []
     closest_names = []
     max_distance = 0
     min_distance = float("inf")

     target = positions[name]
     distance_dic = {}
     for other_name in positions:
          if other_name == name:
               continue
          other_pos = positions[other_name]
          distance = abs(target[0] - other_pos[0]) + abs(target[1] - other_pos[1])
          if sides[name] != sides[other_name]:
               distance += 2
          if distance < min_distance:
               min_distance = distance
          if distance > max_distance:
               max_distance = distance
          distance_dic[other_name] = distance

     for other_name in positions:
          if other_name == name:
               continue
          if distance_dic[other_name] == min_distance:
               closest_names.append(other_name)
          if distance_dic[other_name] == max_distance:
               farthest_names.append(other_name)

     print("最遠" + "、".join(farthest_names) + "；最近" + "、".join(closest_names))
          
print("=========TASK1===========")

func1("辛巴")  # print 最遠弗利沙；最近丁滿、⾙吉塔
 
func1("悟空")  # print 最遠丁滿、弗利沙；最近特南克斯
 
func1("弗利沙")  # print 最遠⾟巴，最近特南克斯
 
func1("特南克斯")  # print 最遠丁滿，最近悟空

# =========TASK2============

booked = {
    "S1": [0] * 25,
    "S2": [0] * 25,
    "S3": [0] * 25
}

def func2(ss, start, end, criteria): 
    # 解析criteria
    if ">=" in criteria:
        field, value = criteria.split(">=")
        op = ">="
    elif "<=" in criteria:
        field, value = criteria.split("<=")
        op = "<="
    else:
        field, value = criteria.split("=")
        op = "="
    if field != "name":
        value = float(value)

    best_service = None
    best_diff = float("inf")

    for s in ss:
        service = s["name"]
        matched = False

        if op == "=":
            if s[field] == value:
                matched = True
        elif op == ">=":
            if s[field] >= value:
                    matched = True
        elif op == "<=":
            if s[field] <= value:
                   matched = True
        
        if not matched:
            continue

        available = True
        for i in range(start, end):
            if booked[service][i] == 1:
                  available = False
                  break
        if not available:
              continue
            
        if field == "name":
            best_service = service
            break
        else:
            diff = abs(s[field] - value)

            if diff < best_diff:
                best_diff = diff
                best_service = service
 
    if best_service == None:
        print("Sorry")
        return
    
    for i in range(start, end):
        booked[best_service][i] = 1
    
    print(best_service)
                 

print("=========TASK2===========")

services=[ 
    {"name":"S1", "r":4.5, "c":1000}, 
    {"name":"S2", "r":3, "c":1200}, 
    {"name":"S3", "r":3.8, "c":800} ]

func2(services, 15, 17, "c>=800")  # S3 
func2(services, 11, 13, "r<=4")  # S3 
func2(services, 10, 12, "name=S3")  # Sorry 
func2(services, 15, 18, "r>=4.5")  # S1 
func2(services, 16, 18, "r>=4")  # Sorry 
func2(services, 13, 17, "name=S1")  # Sorry 
func2(services, 8, 9, "c<=1500")  # S2
func2(services, 8, 9, "c<=1500")    # S1

# =========TASK3============

def func3(index): 
    num = 25
    changes = [-2, -3, 1, 2]
    for i in range(index):
        num += changes[i%4]
    print(num)

print("=========TASK3===========")

func3(1)  # print 23 
func3(5)  # print 21 
func3(10)  # print 16 
func3(30)  # print 6

# =========TASK4============

def func4(sp, stat, n): 
    best_index = -1
    best_diff = n
    for i in range(len(sp)):
        if stat[i] == "0":
            diff = abs(sp[i] - n)
            if diff < best_diff:
                best_diff = diff
                best_index = i
    print(best_index)

print("=========TASK4===========")

func4([3, 1, 5, 4, 3, 2], "101000", 2)  # print 5 
func4([1, 0, 5, 1, 3], "10100", 4)  # print 4 
func4([4, 6, 5, 8], "1000", 4)  # print 2 