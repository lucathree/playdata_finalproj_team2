<script>
	let imgfile, imgtlane, fileinput;
	let result = null,
		resultimg;

	const onFileSelected = (e) => {
		imgfile = e.target.files[0];
		let reader = new FileReader();
		reader.readAsDataURL(imgfile);
		reader.onload = (e) => {
			imgtlane = e.target.result;
		};
	};

	async function doPost() {
		const formData = new FormData();
		formData.append("image", imgfile);

		const res = await fetch("http://localhost:8001/predict", {
			method: "POST",
			//headers: {'Content-Type': 'multipart/form-data'},
			body: formData,
		});

		result = await res.json();

		let baseStr64 = result.image;
		resultimg = "data:image/png;base64," + baseStr64;
	}
</script>

<svelte:head>
	<link
		href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
		rel="stylesheet"
		integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3"
		crossorigin="anonymous"
	/>
</svelte:head>

<div id="frame">
	<div id="header">
		<h1>DESSLA</h1>
	</div>

	<div class="container">
		<div id="before">
			<h4>input</h4>
			{#if imgtlane}
				<img class="imgtlane" src={imgtlane} alt="d" />
			{:else}
				<img
					class="empty"
					src="https://cdn4.iconfinder.com/data/icons/48-bubbles/48/18.Pictures-Day-256.png"
					alt=""
				/>
			{/if}
		</div>

		<div id="after">
			<h4>ouput</h4>
			{#if result}
				<img class="imgtlane" src={resultimg} alt="result" />
			{:else}
				<img
					class="empty"
					src="https://cdn3.iconfinder.com/data/icons/artificial-intelligence-129/512/N_T_1006Artboard_1_copy_12-256.png"
					alt=""
				/>
			{/if}
		</div>
	</div>

	<div id="footer">
		<div id="left">
			<img
				class="upload"
				src="https://static.thenounproject.com/png/625182-200.png"
				alt=""
				on:click={() => {
					fileinput.click();
				}}
			/>
			<div
				class="chan"
				on:click={() => {
					fileinput.click();
				}}
			>
				Choose Image
			</div>
			<input
				style="display:none"
				type="file"
				accept=".jpg, .jpeg, .png"
				on:change={(e) => onFileSelected(e)}
				bind:this={fileinput}
			/>
		</div>

		<div id="right">
			<p />
			<img
				class="upload"
				src="https://st3.depositphotos.com/8950810/17657/v/380/depositphotos_176577870-stock-illustration-cute-smiling-funny-robot-chat.jpg"
				alt=""
				on:click={doPost}
			/>
			Detect lane
		</div>
	</div>
</div>

<style>
	h1 {
		color: #061f56;
		text-transform: uppercase;
		font-size: 3em;
		font-weight: bold;
		text-align: center;
	}

	h4 {
		text-align: center;
	}

	#header {
		border-bottom: 1px solid #ccc;
		padding: 20px 15px;
	}

	#frame {
		width: 1100px;
		height: 812px;
		border: 5px solid #ccc;
		margin: 0 auto;
	}

	#before {
		width: 50%;
		height: 500px;
		border: 2px solid #ccc;
		float: left;
	}

	#after {
		width: 50%;
		height: 500px;
		border: 2px solid #ccc;
		margin-left: auto;
		text-align: center;
	}

	#footer {
		text-align: center;
	}

	.upload {
		display: center;
		height: 60px;
		width: 60px;
		cursor: pointer;
		margin-top: 20px;
	}

	.imgtlane {
		display: flex;
		margin: 0 auto;
		height: 300px;
		width: 500px;
	}

	.empty {
		display: flex;
		height: 150px;
		width: 150px;
		margin-top: 50px;
	}

	#left {
		width: 549px;
		height: 200px;
		border: 2px solid #ccc;
		float: left;
	}

	#right {
		width: 549px;
		height: 200px;
		border: 2px solid #ccc;
		margin-left: 50%;
		margin-bottom: 0%;
	}

	img {
		display: block;
		margin: auto;
	}
</style>
