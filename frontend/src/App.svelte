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
	<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100;300;400;500;700;900&display=swap" rel="stylesheet">
	<style>
		body {
		width: 100;
		height: 100;
		background: linear-gradient(to bottom, rgba(0, 0, 0, 0.1) 30%, rgba(0, 0, 0, 0.4) 65%, #000 120%),  url("/bg4.jpg");
		background-position: center;
		background-size: cover;
		background-attachment: fixed;
		font-family: 'Noto Sans KR', sans-serif;
		}
	</style>
</svelte:head>

<div class="main-container h-10 mt-5 px-3 px-lg-5 mx-auto">
	<img class="img-fluid mt-1" style="width:100px; height:auto;" src="/logo.svg" alt="logo"/>
	<h1 style="font-family:'tesla';">DESLA</h1>
	<div class="row gx-5 justify-content-center row-cols-1 row-cols-lg-2">
		<div class="col">
			<h4 class="py-2">Input</h4>
			<div on:click={() => {fileinput.click();}}>
				{#if imgtlane}
				<div class="imgbox mx-auto bg-transparent d-flex flex-column align-items-center">
					<div class="my-auto">
						<img class="imgtlane rounded" src={imgtlane} alt="input" />
					</div>
				</div>
				<div class="my-auto">
					
				</div>
				{:else}
				<div class="imgbox rounded mx-auto bg-light d-flex flex-column align-items-center">
					<div class="my-auto">
						<img src="/upload.png" style="height:100px; width:auto;" alt=""/>
						<h5 class="pt-2">이미지 업로드</h5>
					</div>
				</div>
				{/if}
			</div>
			<input
				style="display:none"
				type="file"
				accept=".jpg, .jpeg, .png"
				on:change={(e) => onFileSelected(e)}
				bind:this={fileinput}
			/>
		</div>
		<div class="col">
			<h4 class="py-2">Output</h4>
			<div on:click={doPost}>
				{#if result}
					<div class="imgbox mx-auto bg-transparent d-flex flex-column align-items-center">
						<img class="imgtlane rounded" src={resultimg} alt="result" />
					</div>
				{:else}
					<div class="imgbox rounded mx-auto bg-light d-flex flex-column align-items-center">
						<div class="my-auto">
							<img src="/ai.png" style="height:100px; width:auto;" alt=""/>
							<h5 class="pt-2">차선 인식 실행</h5>
						</div>
					</div>
				{/if}
			</div>
		</div>
	</div>
	<div class="annotation row fs-6 text-white justify-content-center mx-auto my-4 bg-secondary" style="--bs-bg-opacity: .4;">
		<div class="col-3 text-center">
			차선인식결과:
		</div>
		<div class="col-2">
			<span style="color:#440053">■</span> 배경 
		</div>
		<div class="col-2">
			<span style="color:#266c8d">■</span> 일반선
		</div>
		<div class="col-2">
			<span style="color:#34ba7d">■</span> 정지선 
		</div>
		<div class="col-3">
			<span style="color:#fde71e">■</span> 횡단보도 
		</div>
	</div>
	<div class="row py-4">
		<img src="/reset.png" style="height:40px; width:auto; cursor:pointer;" alt="" onClick="window.location.reload();"/>
		<div class="reset">초기화</div>
	</div>
</div>
<footer class="text-white text-center">
	<p>Copyright © Playdata Project Team2 SMAO 2021</p>
</footer>

<style>
	@font-face{
		font-family: 'tesla';
		src:url('../fonts/tesla.ttf') format('truetype');
	}

	h1 {
		color: #ab0000;
		text-transform: uppercase;
		font-size: 3em;
		font-weight: bold;
		text-align: center;
	}

	h4 {
		font-weight: bold;
		text-align: center;
	}

	h5 {
		font-weight: bold;
		text-align: center;
	}

	img {
		display: block;
		margin: auto;
	}

	footer {
		margin-top: 40px;
	}

	.main-container {
		max-width: 1080px;
	}

	.imgbox {
		height: 300px;
		max-width: 500px;
		cursor: pointer;
	}

	.imgtlane {
		display: flex;
		margin: 0 auto;
		height: 300px;
		width: 486px;
	}

	.annotation {
		max-width: 600px;
	}

	.reset {
		color: #FFFFFF;
		font-size: 1em;
		letter-spacing: 2px;
		font-weight: bold;
		text-align: center;
	}
/* 
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

	.imgtlane {
		display: flex;
		margin: 0 auto;
		height: 300px;
		width: 500px;
	}

	.upload {
		display: center;
		height: 60px;
		width: 60px;
		cursor: pointer;
		margin-top: 20px;
	}

	.empty {
		display: flex;
		height: 150px;
		width: 150px;
		margin-top: 50px;
	}

*/
</style>
