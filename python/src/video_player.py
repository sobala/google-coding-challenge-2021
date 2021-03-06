"""A video player class."""

from .video_library import VideoLibrary
import numpy as np
from random import randint

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.isPlaying = False
        self.currentlyPlaying = None
        self.isPaused = False
        self.libraryPlaylists = {}
        self.videoList = self._video_library.get_all_videos()
        self.flaggedVideos = {}

    def number_of_videos(self):
        """Returns the number of videos in the library"""

        num_videos = len(self.videoList)
        print(f"{num_videos} videos in the library")

    def display_video_details(self, index):
        """Displays the details of specified video in the format of:
        title (video_id) [tags]

        Args:
            index: The index of video in the library.
        """
        display_format = f"{self.videoList[index].title} "\
        f"({self.videoList[index].video_id}) "\
        f"[{' '.join(map(str, list(self.videoList[index].tags)))}]"

        if self.videoList[index].flag is not None:
            return display_format + f" - FLAGGED (reason: {self.videoList[index].flag})"
        return display_format

    def show_all_videos(self):
        """Returns all videos."""

        print("Here's a list of all available videos:")
        self.videoList.sort(key=lambda x: x.title)
        for index in range(len(self.videoList)):
            print(self.display_video_details(index))

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """

        video = self._video_library.get_video(video_id)
        if video == None:
            print("Cannot play video: Video does not exist")
            return
        if video.flag is not None:
            print(f"Cannot play video: Video is currently flagged (reason: {video.flag})")
            return

        if self.isPlaying == True or self.isPaused == True:
            print("Stopping video: " + self.currentlyPlaying)
        print("Playing video: " + video.title)
        self.currentlyPlaying = video.title
        self.isPlaying = True
        self.isPaused = False

    def stop_video(self):
        """Stops the current playing video."""

        if self.isPlaying == False and self.isPaused == False:
            print("Cannot stop video: No video is currently playing")
        else:
            print("Stopping video: " + self.currentlyPlaying)
            self.isPlaying = False
            self.isPaused = False

    def play_random_video(self):
        """Plays a random video from the video library."""

        video_list_unflagged = []
        for video in self.videoList:
            if video.flag is None:
                video_list_unflagged.append(video)
        if len(video_list_unflagged) == 0:
            print("No videos available")
            return
        random_number = randint(0, len(video_list_unflagged)-1)
        video_random = video_list_unflagged[random_number].title
        if self.isPlaying == True:
            print("Stopping video: " + self.currentlyPlaying)
        print("Playing video: " + video_random)
        self.currentlyPlaying = video_random
        self.isPlaying = True
        self.isPaused = False

    def pause_video(self):
        """Pauses the current video."""

        if self.isPaused == True:
            print("Video already paused: " + self.currentlyPlaying)
        elif self.isPlaying == True:
            print("Pausing video: " + self.currentlyPlaying)
            self.isPlaying = False
            self.isPaused = True
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""

        if self.isPaused == True:
            print("Continuing video: " + self.currentlyPlaying)
            self.isPaused = False
            self.isPlaying = True
        elif self.isPlaying == False:
            print("Cannot continue video: No video is currently playing")
        elif self.isPaused == False:
            print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""

        if self.isPlaying == False and self.isPaused == False:
            print("No video is currently playing")
            return

        for i in range(len(self.videoList)):
            if self.videoList[i].title == self.currentlyPlaying:
                video_current = self.display_video_details(i)

        if self.isPaused == True:
            print(f"Currently playing: {video_current} - PAUSED")
            return
        else:
            print(f"Currently playing: {video_current}")


    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if len(self.libraryPlaylists) == 0:
            self.libraryPlaylists[playlist_name] = []
            print("Successfully created new playlist: " + playlist_name)
        else:
            dic_lower = [k.lower() for k in self.libraryPlaylists.keys()]
            if playlist_name.lower() in dic_lower:
                print("Cannot create playlist: A playlist with the same name already exists")
            else:
                self.libraryPlaylists[playlist_name] = []
                print("Successfully created new playlist: " + playlist_name)

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """

        """Do I need return in each if statement?"""
        try:
            video = self._video_library.get_video(video_id)

            if len(self.libraryPlaylists) == 0:
                print(f"Cannot add video to {playlist_name}: Playlist does not exist")
                return
            else:
                library_playlists_lower = {k.lower():v for k, v in self.libraryPlaylists.items()}
                if playlist_name.lower() not in library_playlists_lower:
                    print(f"Cannot add video to {playlist_name}: Playlist does not exist")
                    return

            if not video:
                print(f"Cannot add video to {playlist_name}: Video does not exist")
                return

            if video.flag is not None:
                print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {video.flag})")
                return
            vids = library_playlists_lower[playlist_name.lower()]

            if video_id in vids:
                print(f"Cannot add video to {playlist_name}: Video already added")
                return
            else:
                for name in self.libraryPlaylists.keys():
                    if name.lower() == playlist_name.lower():
                        self.libraryPlaylists[name].append(video_id)
                        print(f"Added video to {playlist_name}: {video.title}")
        except:
            print("Error")

    def show_all_playlists(self):
        """Display all playlists."""

        if not len(self.libraryPlaylists):
            print("No playlists exist yet")
        else:
            playlists = sorted(self.libraryPlaylists, key=str.casefold)

            print("Showing all playlists:")
            for name in playlists:
                print("\t{}".format(name))

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        playlists = self.libraryPlaylists

        library_playlists_lower = {k.lower():v for k, v in self.libraryPlaylists.items()}
        if  playlist_name.lower() not in library_playlists_lower:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
        elif len(library_playlists_lower[playlist_name.lower()]) == 0:
            print(f"Showing playlist: {playlist_name} \n\tNo videos here yet")
        else:
            print(f"Showing playlist: {playlist_name}")
            for video_iden in library_playlists_lower[playlist_name.lower()]:
                video_object = self._video_library.get_video(video_iden)
                print("\t", self.display_video_details(self.videoList.index(video_object)))

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """

        library_playlists_lower = {k.lower():v for k, v in self.libraryPlaylists.items()}
        if  playlist_name.lower() not in library_playlists_lower:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
            return

        video = self._video_library.get_video(video_id)
        if not video:
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
            return

        if video_id not in library_playlists_lower[playlist_name.lower()]:
            print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            return

        else:
            for name in self.libraryPlaylists.keys():
                if name.lower() == playlist_name.lower():
                    self.libraryPlaylists[name].remove(video_id)
                    print(f"Removed video from {playlist_name}: {video.title}")


    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        library_playlists_lower = {k.lower():v for k, v in self.libraryPlaylists.items()}
        if  playlist_name.lower() not in library_playlists_lower:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
            return

        else:
            for name in self.libraryPlaylists.keys():
                if name.lower() == playlist_name.lower():
                    self.libraryPlaylists[name].clear()
                    print(f"Successfully removed all videos from {playlist_name}")


    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        library_playlists_lower = {k.lower():v for k, v in self.libraryPlaylists.items()}
        if  playlist_name.lower() not in library_playlists_lower:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
            return

        else:
            for name in self.libraryPlaylists.keys():
                if name.lower() == playlist_name.lower():
                    self.libraryPlaylists.pop(name)
                    print(f"Deleted playlist: {playlist_name}")
                    break

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """

        found_titles = []
        for i in range(len(self.videoList)-1):
            if search_term.lower() in self.videoList[i].title.lower() and self.videoList[i].flag is None:
                found_titles.append(self.videoList[i].title)
        if len(found_titles) == 0:
            print(f"No search results for {search_term}")
            return
        else:
            print(f"Here are the results for {search_term}:")
            index = 1
            for name in found_titles:
                for i in range(len(self.videoList)):
                    if self.videoList[i].title.lower() == name.lower():
                        print(f"\t{index}) {self.display_video_details(i)}")
                index = index + 1
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            key = input()
            try:
                key = int(key)
                val = True
            except:
                val = False
            if val and key >= 0 and key <= len(self.videoList)-1:
                video_to_be_played = found_titles[key-1]
                for i in range(len(self.videoList)):
                    if self.videoList[i].title.lower() == video_to_be_played.lower():
                        video = self._video_library.get_video(self.videoList[i].video_id)
                        self.play_video(video.video_id)


    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        found_titles = []
        for i in range(len(self.videoList)-1):
            tags_lower = (t.lower() for t in self.videoList[i].tags)
            if video_tag.lower() in tags_lower and self.videoList[i].flag is None:
                found_titles.append(self.videoList[i].title)
        if len(found_titles) == 0:
            print(f"No search results for {video_tag}")
            return
        else:
            print(f"Here are the results for {video_tag}:")
            index = 1
            for name in found_titles:
                for i in range(len(self.videoList)):
                    if self.videoList[i].title.lower() == name.lower():
                        print(f"\t{index}) {self.display_video_details(i)}")
                index = index + 1
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            key = input()
            try:
                key = int(key)
                val = True
            except:
                val = False
            if val and key >= 0 and key <= len(self.videoList)-1:
                video_to_be_played = found_titles[key-1]
                for i in range(len(self.videoList)):
                    if self.videoList[i].title.lower() == video_to_be_played.lower():
                        video = self._video_library.get_video(self.videoList[i].video_id)
                        self.play_video(video.video_id)

    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """

        video = self._video_library.get_video(video_id)
        if not video:
            print(f"Cannot flag video: Video does not exist")
            return

        if video.flag is not None:
            print("Cannot flag video: Video is already flagged")
            return

        if self.currentlyPlaying == video.title:
            self.stop_video()

        video.set_flag(flag_reason)
        print(f"Successfully flagged video: {video.title} (reason: {flag_reason})")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)
        if video == None:
            print("Cannot remove flag from video: Video does not exist")
            return
        if video.flag is None:
            print("Cannot remove flag from video: Video is not flagged")
            return
        print(f"Successfully removed flag from video: {video.title}")
        video.set_flag(None)
