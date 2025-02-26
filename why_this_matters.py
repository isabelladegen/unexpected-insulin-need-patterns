import streamlit as st


def display_why_this_matters():
    # st.header(why_this_matters)
    st.caption("Our findings have implications for various areas.")

    st.subheader("For Health Care", divider=True)
    st.markdown(
        "Recognise why individualised approaches and patient partnerships are essential for successful T1D management.")
    with st.expander("Explore implications for health care"):
        st.markdown("""
                    #### Treatment diversity
                    - Individual variations exist even among people with excellent glucose control
                    - Unexpected patterns occur as frequently as expected ones
                    - Standard approaches may be ineffective
                    """)
        st.markdown(""" 
                    #### Patient Partnership
                    - Patients that appear "non-compliant" are likely affected by unknown and understudied factors affecting their blood glucose, this label is not helpful 
                    - Blood glucose variations often occur despite best efforts
                    - Unexplained patterns may reflect unknown physiological factors rather than management decisions
                    """)
        st.markdown(""" 
                    #### Care Guidelines
                    - Personalised treatment approaches need to become a priority
                    - Strategies for managing unexpected patterns need to be developed
                    - Collaboration with people with T1D is required to explore solutions while accepting current limitations in understanding
                    - Healthcare systems must provide adequate training, time, and resources for HCPs to implement these approaches
                    """)
    st.subheader("For Policy & Regulation", divider=True)
    st.markdown(
        "Understand why current T1D management approaches are failing to meet targets for the majority of people with T1D.")
    with st.expander("Explore policy implications and opportunities"):
        st.markdown(""" 
                    #### Evidence-Based Policy
                    - Current approaches result in 70% of UK adults with T1D having A1C levels >58 mmol/mol
                    - Only 30% achieve the NICE-recommended target of A1C <48 mmol/mol
                    - Standard guidelines fail to address the reality of unexpected glucose patterns that our research shows are common, not anomalies
                    - Research funding priorities need reassessment given these findings
                    """)
        st.markdown(""" 
                    #### System Change Opportunities
                    - Recognition that unexplained glucose variations are common and not the failure of people with T1D
                    - Investment in personalised approaches and technologies that account for individual variability
                    - Redefining success metrics beyond simplistic targets that don't reflect the complexity revealed by our research
                    """)
        st.markdown("""
                    #### Regulatory Implications
                    - Current approval processes for diabetes technologies may not adequately account for individual variability
                    - Glucose prediction models need to acknowledge limitations given our finding that relationships between insulin, carbohydrates and glucose vary widely
                    - Standards for diabetes management tools should reflect the reality of unexpected patterns
                    """)

    st.subheader("For AI Research", divider=True)
    st.markdown(
        "Understand challenges and opportunities for developing AI methods that can reveal unknown relationships in complex biological systems.")
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

    st.subheader("For T1D Research", divider=True)
    st.markdown(
        "Explore important research questions and methodological considerations arising directly from our findings.")
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
    st.markdown("See how this research may validate what you have known or suspected for a long time.")
    with st.expander("See how this research validates your experience"):
        st.markdown(""" 
                    #### Validation
                    - Scientific evidence confirms unexpected patterns are common
                    - Having more unexpected patterns leads to higher A1C
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
