export const preparedDataHistoryForRequest = (chatHistory) => {
    const dataRequest = []
    for(let i = 0; i < chatHistory.length; i+=2){
        dataRequest.push([chatHistory[i].content, chatHistory[i+1].content])
    }
    return dataRequest
}
