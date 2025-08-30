import streamlit as st

# ページ設定
st.set_page_config(
    page_title="Snowflake クロスワードパズル",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# カスタムCSS
st.markdown("""
<style>
    .crossword-container {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    .crossword-table {
        border-collapse: collapse;
        border: 2px solid #333;
    }
    .crossword-cell {
        width: 45px;
        height: 45px;
        border: 1px solid #666;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        position: relative;
        background-color: white;
    }
    .black-cell {
        background-color: #666 !important;
    }
    .special-cell {
        background-color: #ff6b6b !important;
        color: white !important;
    }
    .number-label {
        font-size: 10px;
        position: absolute;
        top: 2px;
        left: 3px;
        color: red;
        font-weight: normal;
    }
    .special-cell .number-label {
        color: white !important;
    }
    .correct {
        background-color: #90EE90 !important;
    }
    .hint-section {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .hidden-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        opacity: 0.1;
        transition: opacity 0.3s;
    }
    .hidden-button:hover {
        opacity: 1;
    }
    .red-cell-display {
        background-color: #ff6b6b;
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

class SnowflakeCrossword:
    def __init__(self):
        # グリッドサイズ
        self.rows = 9
        self.cols = 13
        
        # 黒マスの位置（1が黒マス）
        self.black_cells = [
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],  # row 0 - HORIZEN
            [1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],  # row 1
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # row 2 - INTELLIGENCE
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],  # row 3
            [1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],  # row 4
            [1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],  # row 5
            [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1],  # row 6
            [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],  # row 7 - SUMMIT
            [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1],  # row 8 - SEARCH
        ]
        
        # 特別なセル（赤背景にする）
        self.special_cells = {
            (1, 8): '1',   # S
            (0, 3): '2',   # I
            (7, 6): '3',   # M
            (5, 1): '4',   # P
            (5, 6): '5',   # L
            (2, 11): '6',  # E
            (8, 0): '7',   # S
            (2, 6): '8',   # I
            (3, 4): '9',   # T
            (5, 9): '10'   # Y
        }
        
        # 答えの定義
        self.answers = {
            'across': {
                '水': {
                    'row': 0, 'col': 0, 'answer': 'HORIZON', 
                    'hint': 'Snowflakeのセマンティックカタログやガバナンス機能をまとめた名称',
                    'label': '水'
                },
                '蟲': {
                    'row': 2, 'col': 0, 'answer': 'INTELLIGENCE', 
                    'hint': '「ビジネス定義を含むビュー」を指すものは何ですか？',
                    'label': '蟲'
                },
                '炎': {
                    'row': 8, 'col': 0, 'answer': 'SEARCH', 
                    'hint': 'Snowfoldの隠れた意識された用語ページ内・AI統合検索の補完機能',
                    'label': '炎'
                },
                '音': {
                    'row': 7, 'col': 4, 'answer': 'SUMMIT', 
                    'hint': 'Snowflake が年に一度開催している、グローバルイベントの名称',
                    'label': '音'
                },
                '恋': {
                    'row': 3, 'col': 2, 'answer': 'DBT', 
                    'hint': 'Snowsightから直接操作できる、データモデルパイプライン構築の統合環境',
                    'label': '恋'
                },
            },
            'down': {
                '蛇': {
                    'row': 0, 'col': 3, 'answer': 'ICEBERG', 
                    'hint': 'Snowflakeがサポートを強化しているオープンテーブルフォーマット',
                    'label': '蛇'
                },
                '風': {
                    'row': 1, 'col': 8, 'answer': 'SEMANTIC', 
                    'hint': '「ビジネス定義を含むビュー」を指すもの',
                    'label': '風'
                },
                '霞': {
                    'row': 1, 'col': 6, 'answer': 'AISQL', 
                    'hint': '自然言語を活用しながらSQLクエリを発行できる機能',
                    'label': '霞'
                },
                '岩': {
                    'row': 1, 'col': 9, 'answer': 'ANALYST', 
                    'hint': 'Snowflake が提供する生成 AI を活用した自然言語分析のためのツール',
                    'label': '岩'
                },
                '雷': {
                    'row': 1, 'col': 1, 'answer': 'SNOWPIPE', 
                    'hint': 'Snowflakeのリアルタイムデータ取り込みを担うサービスでコストが安くなったサービス',
                    'label': '雷'
                },
                '火': {
                    'row': 0, 'col': 11, 'answer': 'OPENFLOW', 
                    'hint': '構造化・非構造化データやバッチ・ストリームの統合を簡素化する機能',
                    'label': '火'
                },
            }
        }
        
        # セッション状態の初期化
        if 'grid' not in st.session_state:
            st.session_state.grid = [['' for _ in range(self.cols)] for _ in range(self.rows)]
        
        if 'revealed' not in st.session_state:
            st.session_state.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        
        if 'completed' not in st.session_state:
            st.session_state.completed = False

    def check_answer(self, direction, key):
        """答えをチェック"""
        if key not in self.answers[direction]:
            return False
            
        answer_info = self.answers[direction][key]
        user_answer = ""
        
        try:
            if direction == 'across':
                for i in range(len(answer_info['answer'])):
                    if answer_info['col'] + i < self.cols:
                        cell_value = st.session_state.grid[answer_info['row']][answer_info['col'] + i]
                        user_answer += cell_value if cell_value else ' '
            else:  # down
                for i in range(len(answer_info['answer'])):
                    if answer_info['row'] + i < self.rows:
                        cell_value = st.session_state.grid[answer_info['row'] + i][answer_info['col']]
                        user_answer += cell_value if cell_value else ' '
        except IndexError:
            return False
        
        return user_answer.upper().strip() == answer_info['answer']

    def set_answer(self, direction, key, user_input):
        """ユーザーの入力をグリッドに設定"""
        if key not in self.answers[direction]:
            return
            
        answer_info = self.answers[direction][key]
        
        try:
            if direction == 'across':
                for i, char in enumerate(user_input.upper()):
                    if i < len(answer_info['answer']) and answer_info['col'] + i < self.cols:
                        if not self.black_cells[answer_info['row']][answer_info['col'] + i]:
                            st.session_state.grid[answer_info['row']][answer_info['col'] + i] = char
            else:  # down
                for i, char in enumerate(user_input.upper()):
                    if i < len(answer_info['answer']) and answer_info['row'] + i < self.rows:
                        if not self.black_cells[answer_info['row'] + i][answer_info['col']]:
                            st.session_state.grid[answer_info['row'] + i][answer_info['col']] = char
        except IndexError:
            pass

    def reveal_answer(self, direction, key):
        """答えを表示"""
        if key not in self.answers[direction]:
            return
            
        answer_info = self.answers[direction][key]
        
        try:
            if direction == 'across':
                for i, char in enumerate(answer_info['answer']):
                    if answer_info['col'] + i < self.cols:
                        st.session_state.grid[answer_info['row']][answer_info['col'] + i] = char
                        st.session_state.revealed[answer_info['row']][answer_info['col'] + i] = True
            else:  # down
                for i, char in enumerate(answer_info['answer']):
                    if answer_info['row'] + i < self.rows:
                        st.session_state.grid[answer_info['row'] + i][answer_info['col']] = char
                        st.session_state.revealed[answer_info['row'] + i][answer_info['col']] = True
        except IndexError:
            pass
    
    def reveal_all_answers(self):
        """すべての答えを表示"""
        for direction in ['across', 'down']:
            for key in self.answers[direction]:
                self.reveal_answer(direction, key)

    def check_completion(self):
        """すべての答えが正解かチェック"""
        for direction in ['across', 'down']:
            for key in self.answers[direction]:
                if not self.check_answer(direction, key):
                    return False
        return True
    
    def get_red_cells_content(self):
        """赤セルの内容を番号順に取得"""
        # 番号を数値としてソート
        sorted_cells = sorted(self.special_cells.items(), key=lambda x: int(x[1]))
        result = []
        all_filled = True
        
        for (row, col), num in sorted_cells:
            content = st.session_state.grid[row][col]
            if content:
                result.append(content)
            else:
                result.append("_")
                all_filled = False
        
        # 文字を連結して表示
        display_text = "".join(result)
        
        # すべて埋まっている場合は特別な表示
        if all_filled:
            return f"✨ {display_text} ✨"
        else:
            return display_text

def main():
    st.title("Snowflake クロスワードパズル")
    st.markdown("### 最終問題：Snowflakeの知識を試そう！")
    
    # パズルインスタンス作成
    puzzle = SnowflakeCrossword()
    
    # メインコンテンツ
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("クロスワードグリッド")
        
        # 赤セルの内容を表示
        red_cells_content = puzzle.get_red_cells_content()
        st.markdown(f'<div class="red-cell-display">キーワード: {red_cells_content}</div>', unsafe_allow_html=True)
        
        # グリッドのHTML生成
        grid_html = '<div class="crossword-container"><table class="crossword-table">'
        
        # ラベル位置の定義（問題番号を含む）
        labels = {}
        for direction in ['across', 'down']:
            for key, info in puzzle.answers[direction].items():
                pos = (info['row'], info['col'])
                if pos not in labels:
                    labels[pos] = info['label']
        
        # 特別なセルのラベルを追加
        for pos, label in puzzle.special_cells.items():
            if pos in labels:
                labels[pos] = labels[pos] + '/' + label  # 既存のラベルがある場合は併記
            else:
                labels[pos] = label
        
        for row in range(puzzle.rows):
            grid_html += '<tr>'
            for col in range(puzzle.cols):
                # セルのクラス設定
                if puzzle.black_cells[row][col] == 1:
                    cell_class = "crossword-cell black-cell"
                    cell_content = ""
                else:
                    # 特別なセルかチェック
                    if (row, col) in puzzle.special_cells:
                        cell_class = "crossword-cell special-cell"
                    else:
                        cell_class = "crossword-cell"
                        if st.session_state.revealed[row][col]:
                            cell_class += " correct"
                    
                    # ラベルの確認
                    label = labels.get((row, col), "")
                    
                    # セルの内容
                    cell_content = st.session_state.grid[row][col]
                    if label:
                        # 特別なセルの場合はラベルの色も変える
                        if (row, col) in puzzle.special_cells:
                            cell_content = f'<span class="number-label" style="color: white !important;">{label}</span>' + cell_content
                        else:
                            cell_content = f'<span class="number-label">{label}</span>' + cell_content
                
                grid_html += f'<td class="{cell_class}">{cell_content}</td>'
            grid_html += '</tr>'
        
        grid_html += '</table></div>'
        st.markdown(grid_html, unsafe_allow_html=True)
        
        # 完成チェック
        if puzzle.check_completion() and not st.session_state.completed:
            st.session_state.completed = True
            st.balloons()
            st.success("おめでとうございます！すべて正解です！")
            st.info("最終動画へアクセス: Snowflakeの知識の柱があなたを待っています！")
    
    with col2:
        st.subheader("答えを入力")
        
        # リセットボタンを上部に配置
        if st.button("🔄 パズルをリセット", type="secondary", use_container_width=True):
            st.session_state.grid = [['' for _ in range(puzzle.cols)] for _ in range(puzzle.rows)]
            st.session_state.revealed = [[False for _ in range(puzzle.cols)] for _ in range(puzzle.rows)]
            st.session_state.completed = False
            st.rerun()
        
        st.divider()
        
        # 横のカギ
        st.markdown("#### 📝 横のカギ")
        direction = 'across'
        for key, info in puzzle.answers[direction].items():
            with st.expander(f"問題 {info['label']}"):
                st.write(info['hint'])
                st.info(f"文字数: {len(info['answer'])}文字")
                
                user_input = st.text_input("答え", key=f"input_across_{key}")
                
                if st.button("✅ チェック", key=f"check_across_{key}"):
                    if user_input:
                        puzzle.set_answer(direction, key, user_input)
                        if puzzle.check_answer(direction, key):
                            st.success("正解！")
                            puzzle.reveal_answer(direction, key)
                            st.rerun()
                        else:
                            st.error("不正解")
        
        st.divider()
        
        # 縦のカギ
        st.markdown("#### 📝 縦のカギ")
        direction = 'down'
        for key, info in puzzle.answers[direction].items():
            with st.expander(f"問題 {info['label']}"):
                st.write(info['hint'])
                st.info(f"文字数: {len(info['answer'])}文字")
                
                user_input = st.text_input("答え", key=f"input_down_{key}")
                
                if st.button("✅ チェック", key=f"check_down_{key}"):
                    if user_input:
                        puzzle.set_answer(direction, key, user_input)
                        if puzzle.check_answer(direction, key):
                            st.success("正解！")
                            puzzle.reveal_answer(direction, key)
                            st.rerun()
                        else:
                            st.error("不正解")
    
    # 隠し全答えボタン（右下に配置）
    st.markdown("""
        <div class="hidden-button">
            <button id="reveal-all" style="padding: 5px 10px; font-size: 10px; opacity: 0.3;">👁️</button>
        </div>
    """, unsafe_allow_html=True)
    
    # 隠しボタンのエリア（右下）
    with st.container():
        cols = st.columns([10, 1])
        with cols[1]:
            if st.button("　", key="hidden_reveal", help="全答え表示"):
                puzzle.reveal_all_answers()
                st.rerun()

if __name__ == "__main__":
    main()
