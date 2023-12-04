import random, math
from itertools import combinations
from shapely.geometry import LineString, Point

# 그을 수 있는 선의 개수를 파악하면 유리하게 가져갈 수 있다.
# 각각의 점에 connected 될 수 있는 갯수
# 남이 삼각형을 만들 수 있으면 나쁜 수
# 게임에서 초반부 중반부에 좋은 규칙
# min-max, 휴리스틱도 중요, tree search
# 너무 순위에만 집착하여 규칙기반으로 하면 안된다
# 게임을 잘 아는게 먼저
# move generator 잘 만들고 휴리스틱 잘 정의
# 규칙은 if, when으로 해도 됨']
# 게임트리 작성해서 게임 만들어봤다.
class MACHINE():
    """
        [ MACHINE ]
        MinMax Algorithm을 통해 수를 선택하는 객체.
        - 모든 Machine Turn마다 변수들이 업데이트 됨

        ** To Do **
        MinMax Algorithm을 이용하여 최적의 수를 찾는 알고리즘 생성
           - class 내에 함수를 추가할 수 있음
           - 최종 결과는 find_best_selection을 통해 Line 형태로 도출
               * Line: [(x1, y1), (x2, y2)] -> MACHINE class에서는 x값이 작은 점이 항상 왼쪽에 위치할 필요는 없음 (System이 organize 함)
    """
    def __init__(self, score=[0, 0], drawn_lines=[], whole_lines=[], whole_points=[], location=[]):
        self.id = "MACHINE"
        self.score = [0, 0] # USER, MACHINE
        self.drawn_lines = [] # Drawn Lines
        self.board_size = 7 # 7 x 7 Matrix
        self.num_dots = 0
        self.whole_points = []
        self.location = []
        self.triangles = [] # [(a, b), (c, d), (e, f)]

    def find_best_selection(self):
        all_endpoints = list(set([point for line in self.drawn_lines for point in line])) # 현재 선분에 포함된 점 리스트
        unconnected_available = [[point1, point2] for (point1, point2) in list(combinations(self.whole_points, 2)) if self.check_availability([point1, point2]) and point1 not in all_endpoints and point2 not in all_endpoints]
        available = [[point1, point2] for (point1, point2) in list(combinations(self.whole_points, 2)) if self.check_availability([point1, point2])]
        if not self.drawn_lines: # 선공일 경우(그려진 선이 없을때)
            scores = [self.calculate_line_score(line) for line in available]
            best_line = available[scores.index(max(scores))]  # 점수가 가장 높은 선분 선택
            print("나 선공")
            return best_line
        elif len(self.drawn_lines) == 1: # 후공일 경우(1개의 선분이 그려져 있을때)
            print("나 후공")
            scores = [self.calculate_line_score(line) for line in unconnected_available]
            best_line = unconnected_available[scores.index(max(scores))]  # 점수가 가장 높은 선분 선택
            return best_line
        else: # 선공, 후공이 아닌 모든 상황
            if unconnected_available: # 연결하지 않는 선분이 남은 경우
                return random.choice(unconnected_available)
            else:
                return random.choice(available)
                    
    def calculate_line_score(self, line): # 선공 시 가장 line_score가 높은 선분을 선택하기 위해 만든 함수(중심과 가장 가깝고 가장 길어야함)
        min_x = min(point[0] for point in self.whole_points)  # 선택된 점들의 최소 x좌표
        max_x = max(point[0] for point in self.whole_points)  # 선택된 점들의 최대 x좌표
        min_y = min(point[1] for point in self.whole_points)  # 선택된 점들의 최소 y좌표
        max_y = max(point[1] for point in self.whole_points)  # 선택된 점들의 최대 y좌표

        center_point = [(min_x + max_x) / 2, (min_y + max_y) / 2]  # 선택된 점들을 포함하는 직사각형의 중심점 계산
        line_center = [(line[0][0] + line[1][0]) / 2, (line[0][1] + line[1][1]) / 2]  # 선분의 중심점 계산
        distance = math.sqrt((line_center[0] - center_point[0])**2 + (line_center[1] - center_point[1])**2)  # 선분의 중심점과 게임판 중심점 간의 거리 계산
        length = math.sqrt((line[0][0] - line[1][0])**2 + (line[0][1] - line[1][1])**2)  # 선분의 길이 계산

        # 선분의 길이에서 선분의 중심점과 게임판 중심점 간의 거리를 뺌
        return length - distance


    
    def check_availability(self, line):
        line_string = LineString(line)

        # Must be one of the whole points
        condition1 = (line[0] in self.whole_points) and (line[1] in self.whole_points)
        
        # Must not skip a dot
        condition2 = True
        for point in self.whole_points:
            if point==line[0] or point==line[1]:
                continue
            else:
                if bool(line_string.intersection(Point(point))):
                    condition2 = False

        # Must not cross another line
        condition3 = True
        for l in self.drawn_lines:
            if len(list(set([line[0], line[1], l[0], l[1]]))) == 3:
                continue
            elif bool(line_string.intersection(LineString(l))):
                condition3 = False

        # Must be a new line
        condition4 = (line not in self.drawn_lines)

        if condition1 and condition2 and condition3 and condition4:
            return True
        else:
            return False    

    
