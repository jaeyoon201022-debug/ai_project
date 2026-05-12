import streamlit as st
st.title('나의 첫 웹서비스 만들기')
a=st.text_input('이름을 입력하세요')
b=st.selectbox('좋아하는 음식을 선택하세요!',['간장게장','간장새우장','마라탕'])
if st.button('인사말 생성'):
  st.write(a+'님, 안녕하세요!')
  st.info(b+'를 좋아하시는군요!')
  st.warning('반가워요!')
  st.error('반가워요!')
  st.ballo
  ons()
