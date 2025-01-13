import streamlit as st

why_do_unexpected_patterns_matter = '''
 > This shows that factors beyond carbohydrates substantially influence blood glucose regulation.
 '''


def display_why_this_matters():
    st.header("Why this matters")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<h3 style='text-align: center;'>For HCP</h3>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("""
                        #### Treatment diversity
                        - Heterogeneous patterns amongst people with T1D with tight control
                        - Unexpected patterns are as common as expected patterns
                        - One-size fits all approaches may harm
                        """)
        with st.container(border=True):
            st.markdown(""" 
                       #### Patient Assessment
                       - Rethink Non-compliance
                       - Consider factors beyond carbohydrates can substantially and frequently influence blood glucose
                       - Expect huge variance among people with T1D
                       """)
        with st.container(border=True):
            st.markdown(""" 
                       #### Care Guidelines
                       - Need for personalisation
                       - Incorporate how to handle unexpected patterns
                       """)
    with col2:
        st.markdown("<h3 style='text-align: center;'>For Researchers</h3>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(""" 
            #### New Questions
            - What factors lead to unexpected patterns?
            - How can we measure and quantify these factors?
            - What leads to the vast diversity in patterns?
            """)
        with st.container(border=True):
            st.markdown(""" 
                   #### Methodology Impact
                   - Find patterns on a per person basis, group afterwards
                   - Predicting blood glucose needs information beyond past glucose, insulin and carb
                   - Predicting blood glucose needs to incorporate that granger causality changes over time
                   """)
    with col3:
        st.markdown("<h3 style='text-align: center;'>For People with T1D</h3>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(""" 
                          #### Validation
                          - There is scientific evidence that unexpected patterns are common in people with tight control
                          """)
        with st.container(border=True):
            st.markdown(""" 
                          #### Outcomes
                          - You might observe blood glucose behaving differently from what is expected
                          - You might need to personalise your treatment to make it work for you
                          - What works one day might not work the next
                          """)
        with st.container(border=True):
            st.markdown(""" 
                          #### Future Care
                          - Non need to let your experience be dismissed
                          - Use our findings to advocate with evidence
                          """)



    st.subheader("Unexpected patterns are as frequent as expected patterns")
    st.markdown(why_do_unexpected_patterns_matter)
    with st.expander("Unexpected patterns explained"):
        st.markdown('''
                Unexpected patterns are times when an increase of insulin doesn't lower blood glucose and/or when eating
                more carbohydrates does not raise blood glucose.
    
                The hormone insulin is expected to enable the cells to take up glucose from the blood which should lead to
                glucose falling. When insulin doesn't lower blood glucose it shows that either more glucose is entering the
                blood stream than the insulin can cover or that other factors make insulin less effective than usually.
    
                Carbohydrates in Type 1 Diabetes lead to glucose raising due to the body not producing the required insulin.
                When carbohydrates don't raise blood glucose it shows that too much insulin has been injected or that
                other factors make insulin more effective than usually.    
            ''')

    st.markdown('''
        > Currently, automated insulin delivery systems are 'flying blind' to these additional factors.
        ''')
    with st.expander("Impact explained"):
        st.markdown('''
                        Due to these additional factor not being systematically quantified and considered in insulin dosing
                        automated insulin delivery systems need to take a cautious approach which can lead to
                        blood glucose levels going out of the healthy range and even require manual interventions from
                        the person with diabetes. Manual interventions in automated insulin delivery can cause the 
                        system to not appropriately asses the situation and can lead to dangerous situations.
                        Manual interventions can also be difficult for the person to deal with.
                    ''')

    st.subheader(
        'Insulin requirements vary wildly between individuals and even for the same individual at different times')
    st.markdown('''
            > This highlights that dynamic and personalised approaches to dosing insulin are essential.
            ''')
