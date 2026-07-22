const signupForm = document.querySelector("#signup-form");

if (signupForm) {
  signupForm.addEventListener("submit", function (event) {
    const name = document.querySelector("#signup-name").value.trim();
    const email = document.querySelector("#signup-email").value.trim();
    const password = document.querySelector("#signup-password").value.trim();

    if (!name || !email || !password) {
      event.preventDefault();
      alert("請填寫所有註冊欄位");
    }
  });
}

const loginForm = document.querySelector("#login-form");

if (loginForm) {
  loginForm.addEventListener("submit", function (event) {
    const email = document.querySelector("#login-email").value.trim();
    const password = document.querySelector("#login-password").value.trim();

    if (!email || !password) {
      event.preventDefault();
      alert("請填寫電子郵件與密碼");
    }
  });
}

const messageForm = document.querySelector("#message-form");
const messageInput = document.querySelector("#message-content");
const messageList = document.querySelector("#message-list");

async function loadMessages() {
  if (!messageList) {
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:3000/api/message", {
      method: "GET",
      credentials: "include",
    });

    const result = await response.json();

    if (result.error) {
      messageList.textContent = "無法取得留言";
      return;
    }

    renderMessages(result.data);
  } catch (error) {
    console.error("Get messages error:", error);
    messageList.textContent = "留言載入失敗";
  }
}

function renderMessages(messages) {
  messageList.innerHTML = "";

  if (messages.length === 0) {
    messageList.textContent = "目前沒有留言";
    return;
  }

  for (const message of messages) {
    const messageItem = document.createElement("div");
    messageItem.className = "message-item";

    const messageText = document.createElement("span");
    messageText.textContent = `${message.name}：${message.content}`;

    messageItem.appendChild(messageText);

    if (message.self) {
      const deleteButton = document.createElement("button");

      deleteButton.type = "button";
      deleteButton.textContent = "刪除";
      deleteButton.className = "delete-button";

      deleteButton.addEventListener("click", async function () {
        const confirmed = confirm("確定要刪除這則留言嗎？");

        if (!confirmed) {
          return;
        }

        await deleteMessage(message.id);
      });

      messageItem.appendChild(deleteButton);
    }

    messageList.appendChild(messageItem);
  }
}

async function deleteMessage(messageId) {
  try {
    const response = await fetch(
      `http://127.0.0.1:3000/api/message/${messageId}`,
      {
        method: "DELETE",
        credentials: "include",
      },
    );

    const result = await response.json();

    if (result.ok) {
      await loadMessages();
    } else {
      alert("留言刪除失敗");
    }
  } catch (error) {
    console.error("Delete message error:", error);
    alert("留言刪除失敗");
  }
}

if (messageForm) {
  messageForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const content = messageInput.value.trim();

    if (!content) {
      alert("請輸入留言內容");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:3000/api/message", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          content: content,
        }),
      });

      const result = await response.json();

      if (result.ok) {
        messageInput.value = "";
        await loadMessages();
      } else {
        alert("留言新增失敗");
      }
    } catch (error) {
      console.error("Create message error:", error);
      alert("留言新增失敗");
    }
  });

  loadMessages();
}
