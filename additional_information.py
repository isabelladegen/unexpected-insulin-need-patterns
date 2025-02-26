import streamlit as st


def display_additional_information():
    st.page_link("https://dx.doi.org/10.2196/44384", label="Read full paper", icon="📖")
    with st.expander("How we analysed the data"):
        st.markdown("""
        We analysed time series data on insulin on board (IOB), carbohydrates on board (COB) and 
        interstitial glucose (IG) from 29 participants using the OpenAPS AID system. 

        **Pattern frequency** in hours, days 
        (grouped via K-means clustering), weekdays, and months were determined by comparing the 95% CI of the mean 
        differences between temporal units.

        **Associations** between pattern frequency and demographic variables were examined. Significant differences in 
        IOB, COB and IG for various time categories were assessed using Mann-Whitney U tests. 
        Effect sizes and Euclidean distances between variables were calculated. Finally, the forecastability of IOB, COB, 
        and IG for the clustered days was analysed using Granger causality. 
        """)
    with st.expander("What makes a pattern unexpected?"):
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
    with st.expander("See who made this research possible"):
        st.markdown("""
                    We would like to thank UK Research and Innovation (UKRI), which is funding author ID's PhD research through the UKRI Doctoral Training in Interactive Artificial Intelligence (AI) under grant EP/S022937/1. 

                    We are grateful to everyone involved in the Interactive AI Centre for Doctoral Training at Bristol University for their support and guidance.

                    We would like to thank Dana Lewis and the entire OpenAPS community, who have tirelessly worked on the open-source automated insulin delivery systems. We would also like to thank the OpenHumans platform for providing the mechanism to donate data, as well as the people with diabetes who have donated their data to research that formed the basis for this study. 

                    We used the generative AI tool Claude Sonnet 3.5 by Anthropic to help with summarising our research content for this demo.
                    """)
