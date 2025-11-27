# PAWSTER
**Overview**
Pawster is a database application with three primary users: animal shelters, animal fosters, and adopters.
Aniaml Shelter: They can sign up and add and remove animal shelter. 
Aniaml Foster: They can sign up and add and remove animals for thier foster home.
Aniaml Users: are able to view animals without signing up and are able to contact a shelter to get in touch and see an animal.
**

# Requirements
This was coded using Python 3.12.4, so you should probably run it using that at minimum. If don't have it installed, here is the [link](https://www.python.org/downloads/release/python-3124/) to download this version. Once you have Python installed, you have two options:
1. Run Requirements.txt in your virtual environment
   
```
$   pip install -r requirements.txt
```

2. Pip install everything one by one in your virtual environment (Because why not do things the hard way)
```
$   pip install Flask
$   pip install flask-login
$   pip install werkzeug
```
# File Structure

```
dog-homing-dogs/Website
│
├── web.py                     # run this to  run everything, creates the app for the API
├── app
|     ├── _pycache_ #   You can ignore this 
|     ├── static
|     |       └── style.css
|     └── templates
|             ├── __init__.py  # You can ignore this 
|             └── api.py       # Api calls 
|
├── animal_shelter.db          # This gets created automatically
├── app.py                     # Where our api is 
└── requirements.txt           # Will need to add this later i think, it was in al lthe examples i could find 
```

**Current Core Features**

- Users can signup with a shelter code to update their local shelter's info
- Shelter owners can make accounts and add their shelter info
- Users can view local shelters without signing up
- Users can view all animals of a shelter without signing up

**Core Features To Be Added**

- Foster Network
- Users can sign up as foster homes.
- Anyone who finds a stray dog can quickly connect with available fosters in their area.
- Rehoming Marketplace
- A platform for rehoming dogs in need of adoption.
- Shelter Availability/Space (Planned Feature)
    
**Purpose**

Too often, stray and surrendered dogs are left without safe options because local shelters are overcrowded. This app provides a community-driven solution by:
  
  - Connecting fosters with people who find strays.
  
  - Providing a safe and reliable way to rehome dogs.
  
  - Offering better visibility into shelter space when available.

**Status**

  This project is in the coding stage. We have it working mostly, but needs some updating 

**Next Steps**

Modify certain aspects to make sure everything works. 
