import streamlit as st

def footer():
    st.sidebar.info("The data is being obtained from the API provided by https://exchangerate.host.")
    
    st.sidebar.markdown("""
    ___
    Collaborations are always welcome!
    <a href="https://github.com/ineelhere/forex-connect" target="_bank" style="text-decoration: none;">
    github.com/ineelhere/forex-connect
    </a>
    [![](https://img.shields.io/github/stars/ineelhere/forex-connect?style=social)](https://github.com/ineelhere/forex-connect) &nbsp; 
    """, unsafe_allow_html=True)


    st.sidebar.markdown("""
    <p class="jumbotron-heading" align='center'>
    Indraneel Chakraborty | 2023
    <br>
    <a href="mailto:hello.indraneel@gmail.com" target="_bank" style="text-decoration: none;">
      <img src="https://freepngimg.com/save-icon/66407-account-icons-wallpaper-desktop-computer-in-sign/512x512" alt="gmail" width="26" height="26">
    </a>
    <a href="https://www.linkedin.com/in/indraneelchakraborty/" target="_bank" style="text-decoration: none;">
      <img src="https://static-exp1.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" alt="Linkedin" width="26" height="26">
    </a>
    <a href="https://sites.google.com/view/indraneelchakraborty" target="_bank" style="text-decoration: none;">
    </a>
    <a href="https://twitter.com/ineelhere" target="_bank" style="text-decoration: none;">
      <img src="https://abs.twimg.com/favicons/twitter.ico" alt="Twitter" width="26" height="26">
    </a>    
    <a href="https://github.com/ineelhere" target="_bank" style="text-decoration: none;">
      <img width="26" height="26" src="https://github.com/fluidicon.png" alt="Github">
    </a>
  </p>""", unsafe_allow_html=True)