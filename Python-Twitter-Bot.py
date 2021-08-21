import tweepy
from tkinter import *
from tkinter import ttk
import tkinter as tk

root=Tk()
root.title("Group H-Twitter Bot")
window=ttk.Frame(root)
canvas=tk.Canvas(window, width=950,height=600)
scrollbar=ttk.Scrollbar(window, orient="vertical",command=canvas.yview)
scrollable_frame=ttk.Frame(canvas)

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.create_window((0,0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)


#Authentication Keys

consumer_key = ''

consumer_secret_key = ''

access_token = ''

access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)

api= tweepy.API(auth,wait_on_rate_limit=True)



#Code for timeline review
def public_tweets():
    text1.delete("1.0","end-1c")
    public_tweets=api.home_timeline()
    for tweet in public_tweets:
        text1.insert("1.0",f"ID:{tweet.id}, {tweet.user.name} said {tweet.text}\n \n")

#Code for updating the timeline status
def update_status():
    status=Tweet_Entry.get("1.0", "end-1c")
    api.update_status(status)

#Code for searching users and get information using code
def get_user():
    Search_Results.delete("1.0","end-1c")
    user_name=Search_Entry.get()
    get_user=api.get_user(user_name)

    S_name=get_user.name
    S_description=get_user.description
    S_location=get_user.location
    Search_Results.insert("1.0","The user details inlcude: \n")

    Search_Results.insert("end","Username: "+S_name+"\n")
    Search_Results.insert("end","Description: "+S_description+"\n")
    Search_Results.insert("end","Location: "+S_location+"\n")
    
    Search_Results.insert("end","The last 20 followers include: \n")
    for follower in get_user.followers():
        Search_Results.insert("end",follower.name+"\n")
        
#Code for followers
def follow():
    api.create_friendship(Follow_Entry.get())
    Follow_Feedback.delete("1.0","end-1c")
    Follow_Feedback.insert("1.0","Followed Successfully")

#Code for Unfollowers
def unfollow():
    api.destroy_friendship(Follow_Entry.get())
    Follow_Feedback.delete("1.0","end-1c")
    Follow_Feedback.insert("1.0","Unfollowed Successfully")

#Code for my account
def update_account_name():
    api.update_profile(name=Name_Entry.get())
    Update_Feedback.delete("1.0","end-1c")
    Update_Feedback.insert("1.0","Name Updated Successfully!")
    
def update_account_location():
    api.update_profile(location=Location_Entry.get())
    Update_Feedback.delete("1.0","end-1c")
    Update_Feedback.insert("1.0","Location Updated Successfully!")

def update_account_description():
    api.update_profile(description=Description_Entry.get())
    Update_Feedback.delete("1.0","end-1c")
    Update_Feedback.insert("1.0","Description Updated Successfully!")

#Code for Like and Dislike
def like():
    tweets=api.get_status(Like_Entry.get())
    tweet=tweets
    api.create_favorite(tweet.id)
    Like_Feedback.delete("1.0","end-1c")
    Like_Feedback.insert("1.0",f"Liking tweet with Id:{tweet.id} of {tweet.author.name}")

def dislike():
    tweets=api.get_status(Like_Entry.get())
    tweet=tweets
    api.destroy_favorite(tweet.id)
    Like_Feedback.delete("1.0","end-1c")
    Like_Feedback.insert("1.0",f"Disliking tweet with Id:{tweet.id} of {tweet.author.name}")

#Code for blocking and viewing blocked users
def block_user():
    api.create_block(Block_Entry.get())
    BlockText.delete("1.0", "end-1c")
    BlockText.insert("1.0","Blocked Successfully!")
    

def unblock_user():
    api.destroy_block(Block_Entry.get())
    BlockText.delete("1.0", "end-1c")
    BlockText.insert("1.0","Unblocked Successfully!")
    

def blocked_user():
    for block in api.blocks():
        BlockText.delete("1.0","end-1c")
        BlockText.insert("1.0",block.name)

#Code for Trending Topics
def trending_topics():
    trending = api.trends_place(1)
    for trend in trending[0]["trends"]:
        Trending_Text.delete("1.0","end-1c")
        Trending_Text.insert("1.0", trend["name"])

#Code for Retweets
def retweet():
    api.retweet(Retweet_Entry.get())
    Retweet_Feedback.delete("1.0","end-1c")
    Retweet_Feedback.insert("1.0","Retweeted Successfully")

#Code for exiting the program
def exit_program():
    root.destroy()
    exit()



#Implementation in Tkinter Interphase

#Logo
Logo=PhotoImage(file="twitter.png")
Label(scrollable_frame, image=Logo, bg="black").pack()

#Display Tweets
WelcomeIntro=Label(scrollable_frame, text="Welcome to Twitter Bot",font=("Harlow Solid Italic", 20)).pack()
HomeTimeline=Label(scrollable_frame, text="Timeline Tweets",font=("Elephant", 15)).pack()
text1= Text(scrollable_frame, height=5, width=100, bd=5, fg="black", padx=20, pady=3, relief="raised",font=("Times New Roman", 13))
text1.pack()
Reload_Tweets=Button(scrollable_frame, text="Refresh Timeline", bd=4, relief="raised", width=20, bg='#00ACEE', font=("Times New Roman", 12), command=public_tweets)
Reload_Tweets.pack()
Space=Label(scrollable_frame).pack()

#Like or Dislike Tweet with ID
Like_Label=Label(scrollable_frame, text="Add ID of tweet to Like or Dislike!", font=("Elephant", 15)).pack()
Like_Entry=Entry(scrollable_frame, width=50, bd=4, relief="sunken", font=("Times New Roman", 15))
Like_Entry.pack()
Like_Feedback_Label=Label(scrollable_frame, text="Like Feedback", font=("Times New Roman", 15)).pack()
Like_Feedback=Text(scrollable_frame, width=50, height=2, bd=4, font=("Times New Roman", 15))
Like_Feedback.pack()
Like_Button=Button(scrollable_frame, text="Like", bd=4, relief="raised", width=20, bg='#00ACEE', font=("Times New Roman", 12), command=like)
Like_Button.pack()
Dislike_Button=Button(scrollable_frame, text="Dislike", bd=4, relief="raised", width=20, bg='#00ACEE', font=("Times New Roman", 12), command=dislike)
Dislike_Button.pack()
Space=Label(scrollable_frame).pack()


#Retweet
Retweet_Label=Label(scrollable_frame, text="Type ID of tweet to retweet", font=("Elephant", 15)).pack()
Retweet_Entry=Entry(scrollable_frame, width=70, bd=4, relief="sunken", font=("Times New Roman", 15))
Retweet_Entry.pack()
Retweet_Button=Button(scrollable_frame, text="Retweet",  bd=4, relief="raised", width=20, bg='#00ACEE', font=("Times New Roman", 12), command=retweet)
Retweet_Button.pack()
Retweet_Feedback_Label=Label(scrollable_frame, text="Retweet Feedback", font=("Times New Roman", 15)).pack()
Retweet_Feedback=Text(scrollable_frame, width=50, height=2, bd=4, font=("Times New Roman", 15))
Retweet_Feedback.pack()
Space=Label(scrollable_frame).pack()


#Update Timeline Tweet
Label1=Label(scrollable_frame, text="Type your tweet here!", font=("Elephant", 15)).pack()
Tweet_Entry=Text(scrollable_frame, width=50, height=5, fg="black", bd=4, font=("Times New Roman", 15))
Tweet_Entry.pack()
update_tweet=Button(scrollable_frame, text="Update", bd=4, relief="raised", width=20, bg='#00ACEE', font=("Times New Roman", 12), command=update_status)
update_tweet.pack()
Space=Label(scrollable_frame).pack()

#Search for user
Search=Label(scrollable_frame, text="Search for user:", font=("Elephant", 15)).pack()
Search_Entry=Entry(scrollable_frame, width=50, fg="black", bd=4, relief="sunken", font=("Times New Roman", 15))
Search_Entry.pack()
Search_user=Button(scrollable_frame, text="Search User", bd=4, relief="raised", width=20, bg='#00ACEE', font=("Times New Roman", 12), command=get_user)
Search_user.pack()
Search_Results=Text(scrollable_frame, height=5, width=90, fg="black", bd=4, font=("Times New Roman", 15))
Search_Results.pack()
Space=Label(scrollable_frame).pack()

#Follow User
Follow=Label(scrollable_frame, text="Type the name to Follow or Unfollow a user!", font=("Elephant", 15)).pack()
Follow_Entry=Entry(scrollable_frame, width=50, bd=4, relief="sunken", font=("Times New Roman", 15))
Follow_Entry.pack()
Follow_Button=Button(scrollable_frame, text="Follow User", bd=4, relief="raised", width=20, bg='#00ACEE', font=("Times New Roman", 12), command=follow)
Follow_Button.pack()

#Unfollow button
Unfollow_Button=Button(scrollable_frame, text="Unfollow User", bd=4, relief="raised", width=20, bg='#00ACEE', font=("Times New Roman", 12), command=unfollow)
Unfollow_Button.pack()
Follow_Feedback_Label=Label(scrollable_frame, text="Follow Feedback", font=("Times New Roman", 15)).pack()
Follow_Feedback=Text(scrollable_frame, width=50, height=2, fg="black", bd=4, font=("Times New Roman", 15))
Follow_Feedback.pack()
Space=Label(scrollable_frame).pack()

#Update User Profile
User_Account=Label(scrollable_frame, text="Update your Account", font=("Elephant", 15)).pack()
I_User_Account=Label(scrollable_frame, text="(Enter either your Name, Location or Description to update your profile at a time!)", font=("Times New Roman", 15)).pack()
Name_Label=Label(scrollable_frame, text="Name", font=("Times New Roman", 15)).pack()
Name_Entry=Entry(scrollable_frame, width=70, bd=4, relief="sunken", font=("Times New Roman", 15))
Name_Entry.pack()
Name_Button=Button(scrollable_frame, text="Update Name", bd=4, relief="raised", width=20, bg='#00ACEE', font=("Times New Roman", 12), command=update_account_name)
Name_Button.pack()
Location_Label=Label(scrollable_frame, text="Location", font=("Times New Roman", 15)).pack()
Location_Entry=Entry(scrollable_frame, width=70, bd=4, relief="sunken", font=("Times New Roman", 15))
Location_Entry.pack()
Location_Button=Button(scrollable_frame, text="Update Location", bd=4, relief="raised", width=20, bg='#00ACEE', font=("Times New Roman", 12), command=update_account_location)
Location_Button.pack()
Description_Label=Label(scrollable_frame, text="Description", font=("Times New Roman", 15)).pack()
Description_Entry=Entry(scrollable_frame, width=70, bd=4, relief="sunken", font=("Times New Roman", 15))
Description_Entry.pack()
Description_Button=Button(scrollable_frame, text="Update Description", bd=4, relief="raised", width=20, bg='#00ACEE', font=("Times New Roman", 12), command=update_account_description)
Description_Button.pack()
Update_Feedback_Label=Label(scrollable_frame, text="Account Update Feedback", font=("Times New Roman", 15)).pack()
Update_Feedback=Text(scrollable_frame, width=70, height=3, fg="black", bd=4, font=("Times New Roman", 15))
Update_Feedback.pack()
Space=Label(scrollable_frame).pack()


#Blocking, Unblocking and Viewing Blocked Users
Block_Label=Label(scrollable_frame, text="Add UserName to Block!", font=("Elephant", 15)).pack()
Block_Entry=Entry(scrollable_frame, width=70, bd=4, relief="sunken", font=("Times New Roman", 15))
Block_Entry.pack()
Block_User=Button(scrollable_frame, text="Block User", bd=4, relief="raised", width=20, bg='#00ACEE', font=("Times New Roman", 12), command=block_user)
Block_User.pack()
Unblock_User=Button(scrollable_frame, text="Unblock User", bd=4, relief="raised", width=20, bg='#00ACEE', font=("Times New Roman", 12), command=unblock_user)
Unblock_User.pack()
BlockText=Text(scrollable_frame, width=70, height=5, fg="black", bd=4, font=("Times New Roman", 15))
BlockText.pack()
View_Block=Button(scrollable_frame, text="View Blocked Users", bd=4, relief="raised", width=20, bg='#00ACEE', font=("Times New Roman", 12), command=blocked_user)
View_Block.pack()
Space=Label(scrollable_frame).pack()


#Trending Topics
Trending_Label=Label(scrollable_frame, text="Trending Topics", font=("Elephant", 15)).pack()
Trending_Text=Text(scrollable_frame, width=50, height=5,  fg="black", bd=4, font=("Times New Roman", 15))
Trending_Text.pack()
Trend_Button=Button(scrollable_frame, text="Trending Topics", bd=4, relief="raised", width=20, bg='#00ACEE', font=("Times New Roman", 12), command=trending_topics)
Trend_Button.pack()
Space=Label(scrollable_frame).pack()


#Exit
Exit=Button(scrollable_frame, text="Exit Program", bd=4, relief="raised", width=20, bg='#00ACEE', font=("Times New Roman", 12), command=exit_program)
Exit.pack()

#Running the main loop
window.pack()
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
root.mainloop()
