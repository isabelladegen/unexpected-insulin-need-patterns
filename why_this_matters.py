import streamlit as st

from constants import why_this_matters

why_do_unexpected_patterns_matter = '''
 > This shows that factors beyond carbohydrates substantially influence blood glucose regulation.
 '''


def display_why_this_matters():
    st.header(why_this_matters)
    st.caption("Our findings have implications for different stakeholders.")

    st.subheader("For Health Care Professional", divider=True)
    with st.expander("Explore implications for your practice"):
        st.markdown("""
                    #### Treatment diversity
                    - Individual variations exist even among people with excellent glucose control
                    - Unexpected patterns occur as frequently as expected ones
                    - Standard approaches may be ineffective
                    """)
        st.markdown(""" 
                    #### Patient Partnership
                    - Do not label patients as "non-compliant" - acknowledge that many factors affecting blood glucose remain unknown and understudied  
                    - Recognise that blood glucose variations often occur despite best efforts
                    - Understand that unexplained patterns may reflect unknown physiological factors rather than management decisions
                    """)
        st.markdown(""" 
                    #### Care Guidelines
                    - Prioritise personalised treatment approaches
                    - Develop strategies for managing unexpected patterns
                    - Work together with the patient to explore solutions while accepting current limitations in understanding
                    """)

    st.subheader("For AI Researchers", divider=True)
    with st.expander("Discover research opportunities"):
        st.markdown("""
                    #### Research Approach
                    - Use AI to uncover evidence of unknown relationships in complex systems where even domain experts lack complete understanding
                    - Focus on unsupervised methods - most biological systems lack ground truth labels
                    - Challenge assumptions that domain expertise alone can validate findings - develop rigorous validation frameworks
                    - Combine AI insights with domain expertise to guide interpretation while remaining open to unexpected discoveries
                    """)
        st.markdown("""
                    #### Methodological Insights
                    - Design unsupervised methods that can:
                      - Detect patterns without requiring labeled data
                      - Handle real-world healthcare data challenges:
                        - Irregular sampling and missing data
                        - Non-normal distributions
                        - Variable-length time series
                        - Complex relationships between variables
                    - Consider individual analysis before group comparisons
                    - Account for temporal variations in relationships between variables
                    """)
        st.markdown("""
                    #### Future Directions
                    - Establish minimum data quality requirements for reliable pattern detection
                    - Develop interpretable unsupervised methods that can distinguish meaningful patterns from arbitrary groupings
                    - Create frameworks for validating unsupervised findings in high-stakes healthcare domains where ground truth may be unknown
                    """)

    st.subheader("For T1D Researchers", divider=True)
    with st.expander("Explore research directions"):
        st.markdown(""" 
                    #### New Research Questions
                    - Identify factors that lead to unexpected patterns in insulin need
                    - Develop methods to measure and quantify these factors
                    - Understand sources of pattern diversity
                    - Incorporate newly identified factors in automated insulin delivery systems
                    """)
        st.markdown(""" 
                    #### Methodology Impact
                    - Prioritise individual analysis before group comparisons to allow for contradictive findings between people
                    - Recognise limitations of current glucose prediction models based on current data not including factors that drive unexpected patterns
                    - Account for temporal changes in glucose regulation
                    """)

    st.subheader("For People with T1D", divider=True)
    with st.expander("See how this research validates your experience"):
        st.markdown(""" 
                    #### Validation
                    - Scientific evidence confirms unexpected patterns are common
                    """)
        st.markdown(""" 
                    #### Understanding Variability
                    - Blood glucose may behave differently than expected
                    - Treatment needs to be personalised
                    - What works today might not work tomorrow - this is normal
                    """)
        st.markdown(""" 
                    #### Advocacy
                    - Your experiences are supported by research but remain understudied
                    - Use these findings to advocate for personalised care
                    """)



