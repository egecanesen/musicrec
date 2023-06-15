# Smart Music Recommendations

## Project Description

The aim of this project is to develop a platform for smart music recommendations. Many popular music streaming platforms utilize recommendation systems, but the inner workings of these systems are often undisclosed. Therefore, the objective of this project was to create a platform where song search can be performed in a more intelligent manner. The project incorporates three different methods for searching songs, providing users with a variety of options.

1. **Million Playlist Dataset (MPD) from Spotify**: In this approach, a word2vec model is employed, treating each playlist as a sentence and each song as a word. The dataset used for this part of the project can be found at the following link [https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge]. By leveraging this dataset, the system generates song recommendations based on the relationships between songs.

2. **Manual Searching**: This method allows users to manually select song attribute values and determine which attributes to consider for the recommendation. Using the chosen attributes, the system identifies the closest neighbors of the selected song and suggests recommendations based on these neighbors.

3. **Search with Song Attributes**: This approach involves extracting song attributes for the desired songs. Once the attributes are obtained, the recommendation process utilizes a similar model as the manual searching method to provide song recommendations.

The main challenge throughout the project was the development of a user interface that integrates the various models created during the course of the project. Only the final selected models, which exhibit good interpretability, were included in this repository. Additionally, different methods for extracting song attributes were experimented with, but the size of the data proved to be a limiting factor.

Throughout the project, I developed my first user interface and gained valuable insights into the fields of recommendation systems and intelligent user interfaces. I discovered the significance of small design choices that can greatly impact the overall interface design.

## Lessons Learned

1. **Music Recommendation Techniques**: I gained a deeper understanding of the different techniques employed in music recommendation systems.

2. **User Interface Design**: Developing the user interface for this project allowed me to explore the critical role of design choices in creating a user-friendly and intuitive platform. I discovered how seemingly minor design decisions can significantly impact the overall user experience.

3. **Data Challenges**: Working with large datasets, such as the Million Playlist Dataset, highlighted the challenges associated with data processing, manipulation, and analysis. I gained experience in handling sizable datasets and addressing related issues.

## Suggestions to Contributors

If any open-source developer wishes to contribute to this project, there are several areas where their help could be valuable:

1. **Spotify Playlist Integration**: The support to extract complete playlists from Spotify would be a valuable addition. This would involve connecting to the Spotify API, retrieving playlist data, and incorporating it into the recommendation process.

2. **Spotify Music Player Integration**: Adding a music player to the platform could help with the process of getting recommendations.

2. **Song Attribute Visualization**: Adding a page dedicated to displaying song attribute plots would enhance the platform's visual representation of the recommendation process. This would provide users with a more comprehensive understanding of how song attributes influence the recommendations.

3. **Improved Recommendations with Song Attributes**: Leveraging the Million Playlist Dataset, scraping song attributes from Spotify, and incorporating these attributes into the recommendation process could lead to more accurate and personalized song suggestions. This would require additional data processing and analysis.

4. **Sound Data and Mel Spectrogram Analysis**: Exploring the potential of using sound data or mel spectrogram transformations to improve prediction accuracy is another avenue for contribution. However, collecting a suitable dataset for this purpose would be necessary.

Contributors are encouraged to explore these suggestions and propose innovative ideas to further enhance the functionality and performance of this app.
