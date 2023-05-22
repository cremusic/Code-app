--- book
INSERT INTO public.book (id, "name", "type", background_image_url,background_color_code,created_date,created_by,modified_date,modified_by) VALUES
	 (1, 'Một chuyến rong chơi', 'SERIES','/images/book-1/cover-name.jpg',0,'2022-02-14 02:47:54.284','system',NULL,NULL);

--- episode
INSERT INTO public.book_episode (id, book_id,"name",author,artist,background_image_url,background_color_code,created_date,created_by,modified_date,modified_by) VALUES
	 (1, 1,'Vũ hội trong vườn','Kat Ha','Xù Mì','/images/book-1/episode-1/cover-name.jpg',0,'2022-02-14 02:56:59.200','system',NULL,NULL),
	 (2, 1,'Giai điệu rừng xanh','Kat Ha','Xù Mì','/images/book-1/episode-2/cover-name.jpg',0,'2022-02-16 10:37:44.026','system',NULL,NULL),
	 (3, 1,'Thanh âm đầm lầy','Kat Ha','Xù Mì','/images/book-1/episode-3/cover-name.jpg',0,'2022-02-16 10:37:44.026','system',NULL,NULL);

--- video
INSERT INTO public.book_episode_video (id, book_episode_id,"name",link,thumbnail, video_id, duration) VALUES
     (1, 1,'Chuột nhắt - Kể chuyện âm nhạc "Vũ hội trong vườn"','https://www.youtube.com/watch?v=Jfx9CbCnUXg&list=PLTA8HvYnbiFFrK1amyyB4QOSDPA8C02Tn','/images/book-1/episode-1/video-1.jpeg', 'Jfx9CbCnUXg', 120),
	 (2, 1,'Khu vườn mùa xuân - Kể chuyện âm nhạc "Vũ hội trong vườn"','https://www.youtube.com/watch?v=TfBA3EXtjy0&list=PLTA8HvYnbiFFrK1amyyB4QOSDPA8C02Tn&index=2','/images/book-1/episode-1/video-2.jpeg', 'TfBA3EXtjy0', 89),
	 (3, 1,'Voi ơi - Kể chuyện âm nhạc "Vũ hội trong vườn"','https://www.youtube.com/watch?v=O9avGp5RVh8&list=PLTA8HvYnbiFFrK1amyyB4QOSDPA8C02Tn&index=3&ab_channel=P%C3%9APP%C3%8DPTV','/images/book-1/episode-1/video-3.jpeg', 'O9avGp5RVh8', 58),
	 (4, 1,'Vũ hội trong vườn - Kể chuyện âm nhạc "Vũ hội trong vườn"','https://www.youtube.com/watch?v=e7YLI1YUnl0&list=PLTA8HvYnbiFFrK1amyyB4QOSDPA8C02Tn&index=4&ab_channel=P%C3%9APP%C3%8DPTV','/images/book-1/episode-1/video-4.jpeg', 'e7YLI1YUnl0', 139),
	 (5, 1,'Khu vườn mùa xuân - Kể chuyện âm nhạc "Vũ hội trong vườn"','https://www.youtube.com/watch?v=H-KJLf7FbxE&list=PLTA8HvYnbiFFrK1amyyB4QOSDPA8C02Tn&index=5&ab_channel=P%C3%9APP%C3%8DPTV','/images/book-1/episode-1/video-5.jpeg', 'H-KJLf7FbxE', 84),
	 (6, 2,'Chim gõ kiến - Kể chuyện âm nhạc "Nhịp điệu rừng xanh"','https://www.youtube.com/watch?v=eR6bWqd9HhY&list=PLTA8HvYnbiFGpHMph-VwxHAjZLvmddFq2&index=1','/images/book-1/episode-2/video-1.jpeg', 'eR6bWqd9HhY', 92),
	 (7, 2,'Chú sâu háu ăn - Kể chuyện âm nhạc "Nhịp điệu rừng xanh"','https://www.youtube.com/watch?v=0QECLwLsWcQ&list=PLTA8HvYnbiFGpHMph-VwxHAjZLvmddFq2&index=2&ab_channel=P%C3%9APP%C3%8DPTV','/images/book-1/episode-2/video-2.jpeg', '0QECLwLsWcQ', 74),
	 (8, 2,'Dậy đi bé yêu - Kể chuyện âm nhạc "Nhịp điệu rừng xanh"','https://www.youtube.com/watch?v=KWrSxJUMyK8&list=PLTA8HvYnbiFGpHMph-VwxHAjZLvmddFq2&index=3&ab_channel=P%C3%9APP%C3%8DPTV','/images/book-1/episode-2/video-3.jpeg', 'KWrSxJUMyK8', 94),
	 (9, 2,'Nhịp điệu rừng xanh - Kể chuyện âm nhạc "Nhịp điệu rừng xanh"','https://www.youtube.com/watch?v=Dox6zDfW3pY&list=PLTA8HvYnbiFGpHMph-VwxHAjZLvmddFq2&index=4&ab_channel=P%C3%9APP%C3%8DPTV','/images/book-1/episode-2/video-4.jpeg', 'Dox6zDfW3pY', 111),
	 (10, 2,'Trò chơi hái táo - Kể chuyện âm nhạc "Nhịp điệu rừng xanh"','https://www.youtube.com/watch?v=GgCRe0RSrdc&list=PLTA8HvYnbiFGpHMph-VwxHAjZLvmddFq2&index=5&ab_channel=P%C3%9APP%C3%8DPTV','/images/book-1/episode-2/video-5.jpeg', 'GgCRe0RSrdc', 65),
	 (11, 2,'Đi hái táo - Kể chuyện âm nhạc "Nhịp điệu rừng xanh"','https://www.youtube.com/watch?v=9wh2TIyMG1M&list=PLTA8HvYnbiFGpHMph-VwxHAjZLvmddFq2&index=6&ab_channel=P%C3%9APP%C3%8DPTV','/images/book-1/episode-2/video-6.jpeg', '9wh2TIyMG1M', 96);
INSERT INTO public.book_episode_video (id, book_episode_id,"name",link,thumbnail, video_id, duration) VALUES
	 (12, 3,'Cơn bão - Kể chuyện âm nhạc "Thanh âm đầm lầy"','https://www.youtube.com/watch?v=DlbRTBcY7D8&list=PLTA8HvYnbiFGybeY5XPV59F6dQ5ide4D1&index=1','/images/book-1/episode-3/video-1.jpeg', 'DlbRTBcY7D8', 101),
	 (13, 3,'Năm chú ễnh ương - Kể chuyện âm nhạc "Thanh âm đầm lầy"','https://www.youtube.com/watch?v=XneIVNe2aEE&list=PLTA8HvYnbiFGybeY5XPV59F6dQ5ide4D1&index=2','/images/book-1/episode-3/video-2.jpeg', 'XneIVNe2aEE', 85),
	 (14, 3,'Chèo bè - Kể chuyện âm nhạc "Thanh âm đầm lầy"','https://www.youtube.com/watch?v=nlkN90GusHY&list=PLTA8HvYnbiFGybeY5XPV59F6dQ5ide4D1&index=3&ab_channel=P%C3%9APP%C3%8DPTV','/images/book-1/episode-3/video-3.jpeg', 'nlkN90GusHY', 94),
	 (15, 3,'Năm chú ếch xanh - Kể chuyện âm nhạc "Thanh âm đầm lầy"','https://www.youtube.com/watch?v=rLSWx4FW9Bg&list=PLTA8HvYnbiFGybeY5XPV59F6dQ5ide4D1&index=4&ab_channel=P%C3%9APP%C3%8DPTV','/images/book-1/episode-3/video-4.jpeg', 'rLSWx4FW9Bg', 175),
	 (16, 3,'Hòa tấu 5 chú ếch xanh - Kể chuyện âm nhạc "Thanh âm đầm lầy"','https://www.youtube.com/watch?v=Q7IzInrP6QU&list=PLTA8HvYnbiFGybeY5XPV59F6dQ5ide4D1&index=5&ab_channel=P%C3%9APP%C3%8DPTV','/images/book-1/episode-3/video-5.jpeg', 'Q7IzInrP6QU', 169);



