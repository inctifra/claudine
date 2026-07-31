// Copyright 2026 liont
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//     https://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import $ from "jquery";


$(async function(){
    const [
        {initializeModalTrigger},
        {setupAjaxForm},
        { toast, ToastProvider }
    ] = await Promise.all([
        import("../../../libs/_modalTrigger"),
        import("../../../libs/formHandler"),
        import("../../../libs/toaster"),
    ])
    const modal = initializeModalTrigger({
        buttonSelector: "button#createStoreButton",
        modalSelector: "#createStoreModal"
    });
    
    ToastProvider("top-center")
    if(modal){
          setupAjaxForm("#createStoreModal form", {
            onSuccess(data) {
              console.log(data)
              const {name} = data
              toast.success("Successful", `Store "${name}" created successfully.`)
              window.location.reload()
            },
            onError(err, {}, form, cleanedError) {
               console.error(cleanedError)
            },
          });
    }


});