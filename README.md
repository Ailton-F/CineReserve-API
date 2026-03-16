## **🏁 DESCRIPTION**

---

The CineReserve API is a high-performance, scalable RESTful backend designed to manage the complexities of modern cinema operations. Built with a focus on data integrity and concurrency control, the system provides a comprehensive portal for movie enthusiasts to discover films, view real-time seat availability, and secure tickets through a robust reservation flow.


## 📄 TECHNICAL REQUIREMENTS

---

**⚙️ [TC.1] API Development:**

* Use **Python 3** and a Python web framework of your choice (**Django REST Framework** preferred).
* Implement the API following RESTful design principles.
* Use **Poetry** for dependency management and packaging.

**🔐 [TC.2] Authentication:**

* Implement **JWT (JSON Web Tokens)** for user authentication and secure session management.

**💽 [TC.3.1] Database:**

* Use a **relational database** (preferably  **PostgreSQL** ).
* Ensure the database design follows best practices, with attention to normalization and performance optimization.

**🔋 [TC.3.2] Caching & Scalability:**

* Implement **Redis** as a distributed lock to manage temporary seat reservations.
* Use **caching** strategies (e.g., Redis) to store popular sessions and improve high-read endpoint performance.

**📄 [TC.4.] Pagination:**

* Implement mandatory pagination for all list-based endpoints (Movies, Sessions, and User Tickets).

**🧪 [TC.5] Testing:**

* Provide **unit tests** (this will be way easier using Django).
* Ensure that both functional and edge cases are well-covered.

**📝 [TC.6] Documentation:**

* API documentation using **Swagger** or  **Postman** .

**🐳 [TC.7] Docker:**

* Containerize the project using  **Docker** . Provide a `Dockerfile` and a `docker-compose.yml` file for a seamless "plug-and-play" setup.

**🔧 [TC.8] Git:**

* Your project must be stored in a public git repository.
* ***Failing this criteria will eliminate you immediately***


## 🌟 BONUS POINTS

---

**👮🏻 Advanced Security Features:**

* Implement **rate limiting** on API endpoints to prevent abuse and scraping.
* Secure endpoints using best practices (input validation, SQL injection prevention, and CSRF protection).

**🔁 Asynchronous Tasks:**

* Use **Celery** (or a similar task queue) to handle background processes, such as auto-releasing expired seat locks and sending confirmation emails.

**🚀 CI/CD:**

* Configure a basic **CI/CD pipeline** (e.g., GitHub Actions, GitLab CI/CD, travis CI or similar) to run automated tests on every push.

## 👨🏼‍🏫 USE CASES

---

Now you are building an API for a local  ***Movie Theater*** *'s *tickets application. This place is called "Cinépolis Natal". This software will use the following APIs:

**CASE 1: Registration and Login**

* Users must be able to sign up via the API by providing an email, username, and password.
* The system must use JWT to manage login sessions and authorize protected requests.

**CASE 2: List all movies available**

* daw

**CASE 3: List all sessions available for a specific movie**

* dawce

CASE 4**: Seat Map Visualization per movie session**

* The system must distinguish between seats that are  **Available** , **Reserved** (temporarily locked), or  **Purchased** .
* All tickets are free

**CASE 5: Reservation & Locking per movie session**

* Upon selecting a seat, the system must trigger a **temporary lock** (e.g., 10-minute timeout).
* This prevents other users from selecting the same seat during the checkout.
* **Note:** Full-time candidates **must** implement this using Redis; Trainees may use a simpler database-level approach if preferred.

**CASE 6: Checkout & Ticket Generation**

* The system processes the order and transitions the reservation from a temporary cache (if a full-time candidate) to a permanent database record.
* There is no payment process. All tickets are ***free***
* A unique digital ticket is generated and linked to the user's account.

**CASE 7: "My Tickets" Portal**

* Authenticated users can list all their purchased tickets.
* The portal must allow users to view active tickets for upcoming movies and their complete purchase history.
