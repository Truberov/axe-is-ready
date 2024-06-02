<template>
  <div>
    <div>
      <div class="tw-text-xl tw-h-[100px] tw-py-5 tw-bg-white tw-fixed tw-w-[510px] tw-top-0 tw-z-10">
        <h1 class="tw-text-primary tw-text-center tw-text-2xl tw-mt-3 tw-font-bold">T-поддержка</h1>

      </div>
      <div class="tw-my-12">
        <div
          v-for="chat in chatTree"
          :key="chat"

        >
          <q-chat-message
            v-if="chat.type === 'ai'"
            class="tw-text-base tw-pr-28 before:tw-content-none"
            bg-color="secondary"
            text-color="black"
          >
            <template v-slot:name>
              <p class="tw-text-sm tw-opacity-50 tw-mb-2">
                Рина
              </p>
            </template>
            <template v-slot:avatar>
              <img
                class="q-message-avatar q-message-avatar--sent tw-mr-4"
                src="~/assets/2d8f34884f7e83fac400bc4758243c45.jpg"
              >
            </template>
            <template #stamp>{{ chat.date ? format(new Date(chat.date), 'HH:mm') : '' }}</template>
            <p class="tw-p-1" v-html="chat.content.replace(/\n/g, '<br>')" />
          </q-chat-message>

          <q-chat-message
            v-else
            class="tw-text-base tw-pl-40 before:tw-content-none"
            bg-color="primary"
            text-color="white"
            sent
          >
            <template v-slot:name>
              <p class="tw-text-sm tw-opacity-50 tw-mb-2">
                Вы
              </p>
            </template>
            <template v-slot:avatar>
            </template>
            <template #stamp>{{ chat.date ? format(new Date(chat.date), 'HH:mm') : '' }}</template>

            <p class="tw-p-1">
              {{ chat.content }}
            </p>
          </q-chat-message>
        </div>
        <q-chat-message
            v-if="loading"
            class="tw-text-base"
            bg-color="secondary"
            text-color="gray"
        >
          <template v-slot:name>
            <strong class="tw-text-sm tw-font-normal tw-opacity-50 tw-mb-2">
              Рина
            </strong>
          </template>
          <template v-slot:avatar>
            <img
                class="q-message-avatar q-message-avatar--sent tw-mr-4"
                src="~/assets/2d8f34884f7e83fac400bc4758243c45.jpg"
            >
          </template>
          <div class="tw-py-1">
            <q-spinner-dots size="2rem" />
          </div>
        </q-chat-message>
      </div>
      <div class="tw-text-xl tw-h-[100px] tw-py-5 tw-bg-white tw-fixed tw-w-[510px] tw-bottom-0">
        <q-input
          :disable="loading"
          @keydown.enter="sendMessage"
          class="tw-bg-white tw-text-lg tw-z-10"
          rounded
          outlined
          v-model="question"
          label="Спросите у ассистента">
          <template #append>
            <q-icon
              class="hover:tw-cursor-pointer"
              color="primary"
              size="md"
              @click="sendMessage"
              :name="mdiArrowRightBoldCircle"
            />
          </template>
        </q-input>
      </div>
    </div>
  </div>
</template>

<script setup>
import { mdiArrowRightBoldCircle } from '@mdi/js';
import { format } from 'date-fns';
import {preparedDataHistoryForRequest} from "~/helper/preparedDataHistoryForRequest.js";
import {getAnswer} from "~/shared/api/index.js";

const chatTree = ref([]);
const question = ref('');
const loading = ref(false);
const chatHistory = [];
async function sendMessage() {
  if (!loading.value) {
    try {
      const message = {
        type: 'user',
        content: `${question.value}`,
        date: new Date(),
      };
      const req = question.value;
      window.scrollTo(0, document.body.scrollHeight);

      question.value = '';
      chatTree.value.push(message);
      window.scrollTo(0, document.body.scrollHeight);

      if (chatTree.value.length === 1) {
        loading.value = true;

        await new Promise((resolve) => {
          setTimeout(() => {
            const hello = {
              type: 'ai',
              content: 'Здравствуйте! Меня зовут Рина. Сейчас я отвечу на ваш вопрос',
              date: new Date(),
            };
            chatTree.value.push(hello);
            resolve(true);
            loading.value = false;
          }, 3000);
        });
      }

        getAnswer(req, chatHistory).then((answer) => {
          const responseMessage = {
            type: 'ai',
            content: answer,
            date: new Date(),
          };
          loading.value = false;

          chatTree.value.push(responseMessage);
          chatHistory.push(message);
          chatHistory.push(responseMessage);
          window.scrollTo(0, document.body.scrollHeight);
        });

      await new Promise((resolve) => {
        setTimeout(() => {
          loading.value = true;
          resolve(true);
        }, 2000);
      });

      // const answer = await new Promise((resolve) => {
      //   setTimeout(() => {
      //     const data = 'Ответ';
      //     resolve(data);
      //   }, 2000);
      // });
    } catch (error) {
      alert(`Join the waiting list if you want to use models: ${error}`);
    }
  }
}
// async function sendMessage() {
//   if (!loading.value) {
//     try {
//       const message = {
//         type: 'human',
//         content: `${question.value}`,
//         date: new Date(),
//       };
//       const questionRequestTemp = question.value
//       question.value = '';
//
//       chatTree.value.push(message);
//
//       window.scrollTo(0, document.body.scrollHeight);
//
//       const response = await fetch('http://10.0.24.81:8080/chat/stream', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//           input: {
//             chat_history: preparedDataHistoryForRequest(chatHistory) || [],
//             question: questionRequestTemp
//           },
//         }),
//       });
//
//       const reader = response.body.getReader();
//       const decoder = new TextDecoder('utf-8');
//       const responseMessage = {
//         type: 'ai',
//         content: '',
//         date: new Date(),
//       };
//       chatTree.value.push(responseMessage);
//       chatHistory.push(message);
//
//       reader.read().then(function processResult(result) {
//         let token = decoder.decode(result.value);
//         console.log(token.split('event: data\r\n')[1])
//         if (token.split('event: data\r\n')[1]) {
//           token = JSON.parse(token.split('event: data\r\ndata: ')[1]);
//           if (token) {
//             chatTree.value.at(-1).content += token;
//             window.scrollTo(0, document.body.scrollHeight);
//           }
//         }
//
//
//         if (result.done) return;
//
//         return reader.read().then(processResult);
//       });
//       chatHistory.push(chatTree.value.at(-1));
//     } catch (error) {
//       alert(`Join the waiting list if you want to use models: ${error}`);
//     }
//   }
// }
</script>
<style>
.q-message-text:last-child:before{
  display: none;
}
.q-message-text--received{
  border-radius: 15px;

}
.q-message-text--sent{
  border-radius: 15px;
}
textarea {
  resize: none;
}

textarea:focus {
  outline: none;
}
</style>
