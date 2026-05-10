import { existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { PythonBridge } from '@interceptor/shared';

let instance: PythonBridge | null = null;

export async function getBridge(): Promise<PythonBridge> {
	if (instance?.isConnected()) return instance;

	const localVenvPython = resolve(import.meta.dirname, '../../../services/python/.venv/bin/python');
	instance = new PythonBridge({
		workerPath: resolve(import.meta.dirname, '../../../services/python/worker.py'),
		pythonPath:
			process.env.PYTHON_PATH ?? (existsSync(localVenvPython) ? localVenvPython : 'python3'),
	});
	await instance.start();
	return instance;
}
